# PicoPanda Game Development Guide

Welcome to PicoPanda game development! This guide will help you create games using Lua for the PicoPanda handheld.

## Getting Started

### 1. Setup Your Development Environment

#### VS Code (Recommended)
`picopanda_api.lua` contains the full API that can be used for game development


### 2. Required Functions

Every PicoPanda game must define these two functions:

```lua
function game_logic_init()
    -- Called once when the game starts
    -- Initialize your game variables here
end

function game_logic_loop()
    -- Called every frame (60 FPS)
    -- Put your game logic and rendering here
end
```

## API Reference

### Input Functions

#### `get_button_status()`
Returns a table with the current state of all buttons.

```lua
local buttons = get_button_status()

if buttons.up then
    -- Up button is pressed
end

if buttons.a then
    -- A button is pressed
end
```

**Available buttons:** `up`, `down`, `left`, `right`, `start`, `select`, `a`, `b`

### Drawing Functions

#### `draw_pixel(x, y, value)`
Draws a single pixel.

```lua
draw_pixel(64, 64, 0x0F)  -- White pixel at center
```

#### `draw_sprite(sprite_size, index, x, y, width, height, flip_x, flip_y)`
Draws a sprite from the sprite sheet.

```lua
-- Draw a 16x16 sprite at position (32, 32)
draw_sprite(16, 0, 32, 32, 16, 16, false, false)
```

**Sprite sizes:** `PIXELS_8x8`, `PIXELS_16x16`, `PIXELS_32x32`

#### `draw_line(x1, y1, x2, y2, value)`
Draws a line between two points.

```lua
draw_line(0, 0, 127, 127, 0x0F)  -- Diagonal line
```

#### `draw_circle(x_center, y_center, radius, filled, value)`
Draws a circle.

```lua
draw_circle(64, 64, 20, true, 0x0F)  -- Filled circle
```

#### `draw_rectangle(x1, y1, width, height, filled, value)`
Draws a rectangle.

```lua
draw_rectangle(10, 10, 50, 30, true, 0x0F)  -- Filled rectangle
```

#### `draw_string(x, y, text, font_index, scale, value)`
Draws text.

```lua
draw_string(0, 0, "Hello World!", 5, 1, 0x0F)
```

### Color Values

The display uses 4-bit greyscale (16 shades):
- `0x00` - Black
- `0x01` - Very Dark Grey
- `0x02` - Dark Grey
- `0x03` - Medium Dark Grey
- `0x04` - Grey
- `0x05` - Medium Grey
- `0x06` - Light Grey
- `0x07` - Very Light Grey
- `0x08` - Off White
- `0x09` - White
- `0x0A` - Bright White
- `0x0B` - Very Bright White
- `0x0C` - Extremely Bright White
- `0x0D` - Nearly Pure White
- `0x0E` - Almost Pure White
- `0x0F` - Pure White

## Display Specifications

- **Resolution:** 128x128 pixels
- **Color depth:** 4-bit greyscale (16 shades)
- **Frame rate:** 60 FPS
- **Coordinate system:** (0,0) at top-left, (127,127) at bottom-right

## Building and Uploading

### Complete Build Process

Follow these steps to compile and upload your game to PicoPanda:

#### 1. Convert Sprite Sheet (if needed)
If you have a C header file (.h) with your sprite sheet data, convert it to binary:
```bash
cd tools
python convert_sprite_sheet.py sprite_sheet.h sprite_sheet.bin
```

**Expected format in .h file:**
```c
uint8_t sprite_sheet[8192] = { 
    0x00, 0x01, 0x02, 0x03, 
    // ... more hex values ...
};
```

#### 2. Build Game Slot Binary
Combine your Lua game code and sprite sheet into a single binary:
```bash
python make_slot_bin.py your_game.lua game_slot.bin game_export.bin
```

**Arguments:**
- `your_game.lua`: Your Lua game file
- `game_slot.bin`: Output binary file
- `game_export.bin`: Combined binary containing sprite sheet, map, and sprite flags (exported from VSCode extension)

#### 3. Upload to PicoPanda
Upload the game binary to your PicoPanda device:
```bash
python upload_game.py -p /dev/ttyACM0 -b 115200 -f game_slot.bin
```

**Arguments:**
- `-p /dev/ttyACM0`: Serial port (adjust for your system)
- `-b 115200`: Baud rate
- `-f game_slot.bin`: Binary file to upload

### Complete Example Workflow

```bash
# 1. Convert sprite sheet
cd tools
python convert_sprite_sheet.py ../my_game/sprites.h sprites.bin

# 2. Build game binary
python make_slot_bin.py ../my_game/game.lua game_slot0.bin sprites.bin

# 3. Upload to device
python upload_game.py -p /dev/ttyACM0 -b 115200 -f game_slot0.bin
```

### Tool Scripts Reference

All tools are located in the `tools/` folder:

- **`convert_sprite_sheet.py`**: Converts C header sprite sheets to binary
- **`make_slot_bin.py`**: Combines Lua code and sprite sheet into game binary
- **`upload_game.py`**: Uploads game binary to PicoPanda via UART
- **`download_game.py`**: Downloads game binary from PicoPanda for verification

Run any script with `-h` for detailed help and usage examples.


### Game not working?
1. Check that both `game_logic_init()` and `game_logic_loop()` are defined
2. Verify sprite sheet format (8192 bytes for 128x128 4-bit)
