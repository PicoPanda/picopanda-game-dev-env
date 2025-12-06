# save as make_slot_bin.py
import sys
import os
import argparse
import re
import subprocess
import tempfile

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
- Lua bytecode data (compiled from source with enums resolved)
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
    
    args = parser.parse_args()
    
    script_path = args.script
    out_path = args.output
    graphics_path = args.graphics
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
    
    # Extract enum mappings from the API file
    api_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "picopanda_api.lua")
    enum_mappings = extract_enums_from_api(api_file_path)
    
    # Read the Lua source file
    print(f"Reading Lua source: {script_path}")
    with open(script_path, "r", encoding="utf-8") as f:
        lua_code = f.read()
    
    # Extract game title from the script
    game_title = extract_game_title(lua_code)
    
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

    # Calculate the total size needed
    total_size = HEADER_SIZE + len(lua_data) + len(graphics_data)

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
    print(f"  Padding: {padding_size} bytes")
    print(f"  Total: {total_size} bytes")
    print("\nMemory layout:")
    print(f"  Lua bytecode length offset: 0x{0:08X}")
    print(f"  Game title offset: 0x{SCRIPT_LENGTH_SIZE:08X}")
    print(f"  Lua bytecode offset: 0x{HEADER_SIZE:08X}")
    print(f"  Sprite sheet offset: 0x{HEADER_SIZE + len(lua_data):08X}")
    print(f"  Tile map offset: 0x{HEADER_SIZE + len(lua_data) + SPRITE_SHEET_SIZE:08X}")
    print(f"  Sprite flags offset: 0x{HEADER_SIZE + len(lua_data) + SPRITE_SHEET_SIZE + TILE_MAP_SIZE:08X}")

if __name__ == "__main__":
    main()