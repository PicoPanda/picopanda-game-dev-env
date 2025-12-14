# save as make_slot_bin.py
import sys
import os
import argparse
import re
import subprocess
import tempfile
import pico8_asset_converter.picopanda as picopanda

def extract_enums_from_api(api_file_path):
    """Extract enum mappings from picopanda_api.lua file"""
    enum_mappings = {}
    
    try:
        with open(api_file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Find all lines that match the pattern: CONSTANT_NAME = number
        # This will match lines like: PIXELS_8x8 = 8
        pattern = r'^(\w+)\s*=\s*(\d+)\s*$'
        matches = re.findall(pattern, content, re.MULTILINE)
        
        for constant_name, numeric_value in matches:
            enum_mappings[constant_name] = numeric_value
            
        print(f"Extracted {len(enum_mappings)} enum constants from {api_file_path}")
        
    except FileNotFoundError:
        print(f"Error: {api_file_path} not found")
        print("The picopanda_api.lua file is required for enum resolution")
        sys.exit(1)
    
    return enum_mappings

def resolve_enums_in_lua(lua_code, enum_mappings):
    """Replace enum constants with their actual numeric values in Lua code"""
    
    # Replace each enum with its numeric value
    for enum_name, numeric_value in enum_mappings.items():
        # Use word boundaries to avoid partial matches
        pattern = r'\b' + re.escape(enum_name) + r'\b'
        lua_code = re.sub(pattern, numeric_value, lua_code)
    
    return lua_code

def compile_lua_to_bytecode(lua_file, output_file=None, strip_debug=True):
    """Compile Lua source to bytecode using luac"""
    if output_file is None:
        output_file = lua_file.replace('.lua', '.luac')
    
    cmd = ['luac']
    if strip_debug:
        cmd.append('-s')
    cmd.extend(['-o', output_file, lua_file])
    
    try:
        subprocess.run(cmd, check=True)
        return output_file
    except subprocess.CalledProcessError as e:
        print(f"Error compiling Lua file: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("Error: luac not found. Make sure Lua is installed and in your PATH.")
        print("Install Lua: brew install lua (macOS) or apt-get install lua5.1 (Linux)")
        sys.exit(1)

def find_require_and_dofile_calls(lua_code):
    """Find all require() and dofile() calls in Lua code"""
    dependencies = []
    
    # Pattern for require("module") or require('module')
    require_pattern = r'require\s*\(\s*["\']([^"\']+)["\']\s*\)'
    # Pattern for dofile("file.lua") or dofile('file.lua')
    dofile_pattern = r'dofile\s*\(\s*["\']([^"\']+)["\']\s*\)'
    
    # Find all require calls
    for match in re.finditer(require_pattern, lua_code):
        module_path = match.group(1)
        start_pos = match.start()
        end_pos = match.end()
        
        # Check if there's an assignment before this require call
        # Look backwards for "local var = " pattern
        before_text = lua_code[max(0, start_pos-50):start_pos]
        assignment_match = re.search(r'(local\s+\w+\s*=\s*)$', before_text)
        assignment = assignment_match.group(1) if assignment_match else None
        
        if assignment:
            # Include the assignment in the range
            start_pos = start_pos - len(assignment)
        
        dependencies.append(('require', module_path, start_pos, end_pos, assignment))
    
    # Find all dofile calls
    for match in re.finditer(dofile_pattern, lua_code):
        file_path = match.group(1)
        dependencies.append(('dofile', file_path, match.start(), match.end(), None))
    
    return dependencies

def resolve_file_path(module_path, base_dir, script_path):
    """Resolve a module/file path to an actual file path"""
    script_dir = os.path.dirname(script_path)
    possible_paths = []
    
    # If it's a require() call, try common Lua module resolution
    if not module_path.endswith('.lua'):
        # Try various path combinations
        # 1. Direct path with .lua extension
        possible_paths.append(os.path.join(base_dir, module_path + '.lua'))
        # 2. Dot notation converted to path separators
        possible_paths.append(os.path.join(base_dir, module_path.replace('.', os.sep) + '.lua'))
        # 3. In a subdirectory
        possible_paths.append(os.path.join(base_dir, module_path, 'init.lua'))
        # 4. Relative to script directory
        possible_paths.append(os.path.join(script_dir, module_path + '.lua'))
        possible_paths.append(os.path.join(script_dir, module_path.replace('.', os.sep) + '.lua'))
    else:
        # It's already a file path
        possible_paths.append(os.path.join(base_dir, module_path))
        possible_paths.append(os.path.join(script_dir, module_path))
        # Try relative path
        if not os.path.isabs(module_path):
            possible_paths.append(os.path.join(os.getcwd(), module_path))
    
    # Try each possible path
    for path in possible_paths:
        abs_path = os.path.abspath(path)
        if os.path.exists(abs_path):
            return abs_path
    
    # Not found
    return None

def bundle_lua_files(script_path, visited=None):
    """Recursively bundle Lua files, inlining require() and dofile() calls"""
    if visited is None:
        visited = set()
    
    script_path = os.path.abspath(script_path)
    
    # Check for circular dependencies
    if script_path in visited:
        print(f"Warning: Circular dependency detected for {script_path}, skipping")
        return ""
    
    visited.add(script_path)
    
    # Read the file
    try:
        with open(script_path, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: File not found: {script_path}")
        return ""
    
    base_dir = os.path.dirname(script_path)
    
    # Find all require() and dofile() calls
    dependencies = find_require_and_dofile_calls(content)
    
    if not dependencies:
        # No dependencies, return content as-is
        return content
    
    # Process dependencies in reverse order to maintain correct replacement positions
    dependencies.sort(key=lambda x: x[2], reverse=True)
    
    bundled_content = content
    for dep_info in dependencies:
        if len(dep_info) == 5:
            dep_type, module_path, start_pos, end_pos, assignment = dep_info
        else:
            # Backward compatibility
            dep_type, module_path, start_pos, end_pos = dep_info
            assignment = None
        
        # Resolve the file path
        file_path = resolve_file_path(module_path, base_dir, script_path)
        
        if file_path and os.path.exists(file_path):
            print(f"  Bundling {dep_type}: {module_path} -> {file_path}")
            # Recursively bundle the dependency
            bundled_dep = bundle_lua_files(file_path, visited.copy())
            
            # Check if the bundled file returns a module (has a return statement)
            has_return = bool(re.search(r'\breturn\s+', bundled_dep.strip(), re.MULTILINE))
            
            if assignment:
                # There's an assignment like "local x = require(...)"
                var_match = re.search(r'local\s+(\w+)\s*=', assignment)
                var_name = var_match.group(1) if var_match else None
                
                if has_return:
                    # File returns a module, wrap it to capture the return value
                    replacement = f"\n-- Begin bundled: {os.path.basename(file_path)}\nlocal {var_name} = (function()\n{bundled_dep}\nend)()\n-- End bundled: {os.path.basename(file_path)}\n"
                else:
                    # File doesn't return a module
                    # Inline the content and create an empty module table
                    # Functions will be in global scope, but we create the table for compatibility
                    replacement = f"\n-- Begin bundled: {os.path.basename(file_path)}\n{bundled_dep}\nlocal {var_name} = {{}}\n-- Note: Functions from {os.path.basename(file_path)} are in global scope\n-- End bundled: {os.path.basename(file_path)}\n"
                # Remove the entire assignment line
                bundled_content = bundled_content[:start_pos] + replacement + bundled_content[end_pos:]
            else:
                # No assignment, just replace the require/dofile call
                # Wrap in a do...end block to create a local scope
                replacement = f"\n-- Begin bundled: {os.path.basename(file_path)}\ndo\n{bundled_dep}\nend\n-- End bundled: {os.path.basename(file_path)}\n"
                bundled_content = bundled_content[:start_pos] + replacement + bundled_content[end_pos:]
        else:
            print(f"Warning: Could not resolve {dep_type} '{module_path}' in {script_path}")
            # Remove the require/dofile call (comment it out)
            if assignment:
                # Remove the entire assignment line
                bundled_content = bundled_content[:start_pos] + f"-- require/dofile not found: {module_path}\n" + bundled_content[end_pos:]
            else:
                bundled_content = bundled_content[:start_pos] + f"-- require/dofile not found: {module_path}\n" + bundled_content[end_pos:]
    
    return bundled_content

def extract_game_title(lua_code):
    """Extract game title from Lua script"""
    game_title = ""
    
    # Look for game_title variable declarations
    # Support multiple quote styles: "title", 'title', [[title]]
    patterns = [
        r'game_title\s*=\s*["\']([^"\']+)["\']',  # "title" or 'title'
        r'game_title\s*=\s*\[\[([^\]]+)\]\]',      # [[title]]
    ]
    
    for pattern in patterns:
        match = re.search(pattern, lua_code, re.IGNORECASE)
        if match:
            game_title = match.group(1).strip()
            print(f"Found game title: '{game_title}'")
            break
    
    if not game_title:
        print("No game_title found in script, using default")
        game_title = "Untitled Game"
    
    return game_title

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Create a PicoPanda game slot binary from Lua script and graphics binary",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --script game.lua --output game_slot.bin
  %(prog)s --script game.lua --output game_slot.bin --graphics graphics.bin
  %(prog)s -s game.lua -o game_slot.bin -g graphics.bin
  %(prog)s -h

The script creates a 128KB binary file containing:
- 4-byte Lua script length
- 32-byte game title (null-terminated, padded with 0x00)
- Lua bytecode data (bundled from multiple files, enums resolved, then compiled)
- Graphics binary (consisting of):
  * 8192-byte sprite sheet (128x128 pixels, 4-bit greyscale)
  * 8192-byte tile map (128x64 tiles, 1 byte per tile)
  * 256-byte sprite flags (1 byte per sprite, 8 flags per byte)
- Padding to fill 128KB slot
        """
    )
    
    # Required arguments
    parser.add_argument("-s", "--script", required=True, 
                       help="Input Lua script file")
    parser.add_argument("-o", "--output", required=True, 
                       help="Output binary file")
    
    # Optional arguments
    parser.add_argument("-g", "--graphics", 
                       help="Input graphics binary file (creates default if not provided)")
    parser.add_argument("-a", "--audio", 
                       help="Input audio binary file (creates default if not provided)")
    
    args = parser.parse_args()
    
    script_path = args.script
    out_path = args.output
    graphics_path = args.graphics
    audio_path = args.audio
    slot_size = 0x20000  # 128KB
    
    # Binary section sizes
    SCRIPT_LENGTH_SIZE = 4
    GAME_TITLE_SIZE = 32
    HEADER_SIZE = SCRIPT_LENGTH_SIZE + GAME_TITLE_SIZE
    
    # Graphics binary section sizes
    SPRITE_SHEET_SIZE = 8192      # 128x128 pixels at 4 bits per pixel
    TILE_MAP_SIZE = 8192          # 128x64 tiles, 1 byte per tile
    SPRITE_FLAGS_SIZE = 256       # 256 sprites, 1 byte per sprite
    GRAPHICS_BINARY_SIZE = SPRITE_SHEET_SIZE + TILE_MAP_SIZE + SPRITE_FLAGS_SIZE  # 16,640 bytes
    AUDIO_PHRASE_DATA_SIZE = 768
    AUDIO_NOTE_DATA_SIZE = 8192
    AUDIO_BINARY_SIZE =  AUDIO_NOTE_DATA_SIZE + AUDIO_PHRASE_DATA_SIZE
    
    # Extract enum mappings from the API file
    api_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "picopanda_api.lua")
    enum_mappings = extract_enums_from_api(api_file_path)
    
    # Read the Lua source file
    print(f"Reading Lua source: {script_path}")
    script_path = os.path.abspath(script_path)
    
    # Extract game title from the original script (before bundling)
    with open(script_path, "r", encoding="utf-8") as f:
        original_code = f.read()
    game_title = extract_game_title(original_code)
    
    # Bundle all Lua files (resolve require() and dofile() calls)
    print("Bundling Lua files...")
    lua_code = bundle_lua_files(script_path)
    
    # Resolve enums to numeric values
    print("Resolving enum constants...")
    lua_code = resolve_enums_in_lua(lua_code, enum_mappings)
    
    # Write resolved code to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.lua', delete=False) as tmp_file:
        tmp_file.write(lua_code)
        tmp_file_path = tmp_file.name
    
    # Create temporary file for bytecode output
    with tempfile.NamedTemporaryFile(suffix='.luac', delete=False) as tmp_bytecode:
        bytecode_file = tmp_bytecode.name
    
    try:
        # Compile to bytecode
        print("Compiling to bytecode...")
        compile_lua_to_bytecode(tmp_file_path, bytecode_file, strip_debug=True)
        
        # Read the compiled bytecode
        with open(bytecode_file, "rb") as f:
            lua_data = f.read()
    finally:
        # Clean up temporary files
        if os.path.exists(tmp_file_path):
            os.unlink(tmp_file_path)
        if os.path.exists(bytecode_file):
            os.unlink(bytecode_file)
    
    # Prepare game title data (32 bytes, null-terminated, padded with 0x00)
    title_bytes = game_title.encode('utf-8')
    if len(title_bytes) > GAME_TITLE_SIZE - 1:  # -1 for null terminator
        title_bytes = title_bytes[:GAME_TITLE_SIZE - 1]
        print(f"Warning: Game title truncated to '{title_bytes.decode('utf-8')}'")
    
    # Pad title to exactly 32 bytes
    title_data = title_bytes + b'\x00' + b'\x00' * (GAME_TITLE_SIZE - len(title_bytes) - 1)

    # Read the graphics binary if provided
    graphics_data = None
    if graphics_path and os.path.exists(graphics_path):
        with open(graphics_path, "rb") as f:
            graphics_data = f.read()
            if len(graphics_data) != GRAPHICS_BINARY_SIZE:
                print(f"Warning: Graphics binary size is {len(graphics_data)} bytes, expected {GRAPHICS_BINARY_SIZE}")
                print(f"Expected breakdown: {SPRITE_SHEET_SIZE} + {TILE_MAP_SIZE} + {SPRITE_FLAGS_SIZE} = {GRAPHICS_BINARY_SIZE}")
                # Pad or truncate to correct size
                if len(graphics_data) < GRAPHICS_BINARY_SIZE:
                    graphics_data += b'\x00' * (GRAPHICS_BINARY_SIZE - len(graphics_data))
                    print(f"Padded graphics binary to {len(graphics_data)} bytes")
                else:
                    graphics_data = graphics_data[:GRAPHICS_BINARY_SIZE]
                    print(f"Truncated graphics binary to {len(graphics_data)} bytes")
    else:
        # Create a default graphics binary if none provided
        print("No graphics binary provided, creating default pattern")
        
        # Create default sprite sheet
        print("  Creating default sprite sheet...")
        sprite_data = b''
        for i in range(SPRITE_SHEET_SIZE):
            # Create a simple alternating pattern
            if (i // 64) % 2 == 0:  # Every 64 bytes (32 pixels) alternate
                sprite_data += bytes([0x0F if i % 2 == 0 else 0xF0])
            else:
                sprite_data += bytes([0xF0 if i % 2 == 0 else 0x0F])
        
        # Create default tile map (all transparent/empty tiles)
        print("  Creating default tile map (all tiles transparent)...")
        tile_map_data = b'\xFF' * TILE_MAP_SIZE  # 255 = transparent/empty
        
        # Create default sprite flags (all flags cleared)
        print("  Creating default sprite flags (all flags cleared)...")
        sprite_flags_data = b'\x00' * SPRITE_FLAGS_SIZE  # All flags set to 0
        
        # Combine all graphics sections
        graphics_data = sprite_data + tile_map_data + sprite_flags_data

    # Read the audio binary if provided
    audio_data = None
    if audio_path and os.path.exists(audio_path):
        with open(audio_path, "rb") as f:
            audio_data = f.read()
            if len(audio_data) != AUDIO_BINARY_SIZE:
                print(f"Warning: Audio binary size is {len(audio_data)} bytes, expected {AUDIO_BINARY_SIZE}")
                print(f"Expected breakdown: {AUDIO_PHRASE_DATA_SIZE} + {AUDIO_NOTE_DATA_SIZE}")
                # Pad or truncate to correct size
                if len(audio_data) < AUDIO_BINARY_SIZE:
                    audio_data += b'\x00' * (AUDIO_BINARY_SIZE - len(audio_data))
                    print(f"Padded audio binary to {len(audio_data)} bytes")
                else:
                    audio_data = audio_data[:AUDIO_BINARY_SIZE]
                    print(f"Truncated audio binary to {len(audio_data)} bytes")
    else:
        # Create a default audio binary if none provided
        print("No audio binary provided, creating default pattern")
        
        phrase_data = bytearray()
        note_data = bytearray()
        empty_phrase = picopanda.Phrase(0)
        empty_phrase.addEmptyNotes()
        for i in range(256):
            phrase_data += empty_phrase.phraseDataToByteArray()
        for i in range(64):
            note_data += empty_phrase.noteDataToByteArray()
        audio_data = note_data + phrase_data


    # Calculate the total size needed
    total_size = HEADER_SIZE + len(lua_data) + len(graphics_data) + len(audio_data)

    if total_size > slot_size:
        print(f"Error: Total size {total_size} exceeds slot size {slot_size}")
        sys.exit(1)

    # Write the binary
    with open(out_path, "wb") as out:
        # Write Lua script length
        out.write(len(lua_data).to_bytes(4, "little"))
        
        # Write game title (32 bytes)
        out.write(title_data)
        
        # Write Lua script
        out.write(lua_data)
        
        # Write graphics binary (sprite sheet + tile map + sprite flags)
        out.write(graphics_data)
        
        # Write audio binary (notes + phraseData)
        out.write(audio_data)

        # Pad with 0xFF to 128KB
        padding_size = slot_size - total_size
        out.write(b'\xFF' * padding_size)

    print("\nCreated game slot binary:")
    print(f"  Lua bytecode: {len(lua_data)} bytes")
    print(f"  Game title: '{game_title}' ({GAME_TITLE_SIZE} bytes)")
    print(f"  Graphics binary: {len(graphics_data)} bytes")
    print(f"    ├─ Sprite sheet: {SPRITE_SHEET_SIZE} bytes")
    print(f"    ├─ Tile map: {TILE_MAP_SIZE} bytes")
    print(f"    └─ Sprite flags: {SPRITE_FLAGS_SIZE} bytes")
    print(f"  Audio binary: {len(audio_data)} bytes")
    print(f"    ├─ Note Data: {AUDIO_NOTE_DATA_SIZE} bytes")
    print(f"    ├─ Phrase Data: {AUDIO_PHRASE_DATA_SIZE} bytes")
    print(f"  Padding: {padding_size} bytes")
    print(f"  Total: {total_size} bytes")
    print("\nMemory layout:")
    print(f"  Lua bytecode length offset: 0x{0:08X}")
    print(f"  Game title offset: 0x{SCRIPT_LENGTH_SIZE:08X}")
    print(f"  Lua bytecode offset: 0x{HEADER_SIZE:08X}")
    print(f"  Sprite sheet offset: 0x{HEADER_SIZE + len(lua_data):08X}")
    print(f"  Tile map offset: 0x{HEADER_SIZE + len(lua_data) + SPRITE_SHEET_SIZE:08X}")
    print(f"  Sprite flags offset: 0x{HEADER_SIZE + len(lua_data) + SPRITE_SHEET_SIZE + TILE_MAP_SIZE:08X}")
    print(f"  Note data offset: 0x{HEADER_SIZE + len(lua_data) + SPRITE_SHEET_SIZE + TILE_MAP_SIZE + SPRITE_FLAGS_SIZE:08X}")
    print(f"  Phrase data offset: 0x{HEADER_SIZE + len(lua_data) + SPRITE_SHEET_SIZE + TILE_MAP_SIZE + SPRITE_FLAGS_SIZE + AUDIO_NOTE_DATA_SIZE:08X}")

if __name__ == "__main__":
    main()