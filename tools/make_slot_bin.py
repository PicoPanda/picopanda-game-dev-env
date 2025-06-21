# save as make_slot_bin.py
import sys
import os
import argparse
import re

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

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Create a PicoPanda game slot binary from Lua script and sprite sheet",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s game.lua game_slot.bin
  %(prog)s game.lua game_slot.bin sprites.bin
  %(prog)s -h

The script creates a 128KB binary file containing:
- 4-byte Lua script length
- Lua script data (with enums resolved to numeric values)
- 8192-byte sprite sheet (128x128 pixels, 4-bit greyscale)
- Padding to fill 128KB slot
        """
    )
    
    parser.add_argument("script", help="Input Lua script file")
    parser.add_argument("output", help="Output binary file")
    parser.add_argument("sprite_sheet", nargs="?", help="Input sprite sheet file (optional, creates default if not provided)")
    
    args = parser.parse_args()
    
    script_path = args.script
    out_path = args.output
    sprite_sheet_path = args.sprite_sheet
    slot_size = 0x20000  # 128KB
    SPRITE_SHEET_SIZE = 8192  # 128x128 pixels at 4 bits per pixel

    # Extract enum mappings from the API file
    api_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "picopanda_api.lua")
    enum_mappings = extract_enums_from_api(api_file_path)

    # Read the Lua script as text first
    with open(script_path, "r", encoding="utf-8") as f:
        lua_code = f.read()

    # Resolve enums to numeric values
    lua_code = resolve_enums_in_lua(lua_code, enum_mappings)
    
    # Convert to bytes for binary output
    lua_data = lua_code.encode('utf-8')

    # Read the sprite sheet if provided
    sprite_data = None
    if sprite_sheet_path and os.path.exists(sprite_sheet_path):
        with open(sprite_sheet_path, "rb") as f:
            sprite_data = f.read()
            if len(sprite_data) != SPRITE_SHEET_SIZE:
                print(f"Warning: Sprite sheet size is {len(sprite_data)} bytes, expected {SPRITE_SHEET_SIZE}")
                # Pad or truncate to correct size
                if len(sprite_data) < SPRITE_SHEET_SIZE:
                    sprite_data += b'\x00' * (SPRITE_SHEET_SIZE - len(sprite_data))
                else:
                    sprite_data = sprite_data[:SPRITE_SHEET_SIZE]
    else:
        # Create a default sprite sheet if none provided
        print("No sprite sheet provided, creating default pattern")
        sprite_data = b''
        for i in range(SPRITE_SHEET_SIZE):
            # Create a simple alternating pattern
            if (i // 64) % 2 == 0:  # Every 64 bytes (32 pixels) alternate
                sprite_data += bytes([0x0F if i % 2 == 0 else 0xF0])
            else:
                sprite_data += bytes([0xF0 if i % 2 == 0 else 0x0F])

    # Calculate the total size needed
    total_size = 4 + len(lua_data) + SPRITE_SHEET_SIZE

    if total_size > slot_size:
        print(f"Error: Total size {total_size} exceeds slot size {slot_size}")
        sys.exit(1)

    # Write the binary
    with open(out_path, "wb") as out:
        # Write Lua script length
        out.write(len(lua_data).to_bytes(4, "little"))
        
        # Write Lua script
        out.write(lua_data)
        
        # Write sprite sheet
        out.write(sprite_data)
        
        # Pad with 0xFF to 128KB
        padding_size = slot_size - total_size
        out.write(b'\xFF' * padding_size)

    print(f"Created game slot binary:")
    print(f"  Lua script: {len(lua_data)} bytes")
    print(f"  Sprite sheet: {len(sprite_data)} bytes")
    print(f"  Padding: {padding_size} bytes")
    print(f"  Total: {total_size} bytes")
    print(f"  Sprite sheet offset: 0x{4 + len(lua_data):08X}")

if __name__ == "__main__":
    main()