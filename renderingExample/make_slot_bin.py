# save as make_slot_bin.py
import sys
import os

script_path = sys.argv[1]
out_path = sys.argv[2]
sprite_sheet_path = sys.argv[3] if len(sys.argv) > 3 else None
slot_size = 0x20000  # 128KB
SPRITE_SHEET_SIZE = 8192  # 128x128 pixels at 4 bits per pixel

# Read the Lua script
with open(script_path, "rb") as f:
    lua_data = f.read()

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