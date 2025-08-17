# PicoPanda Game Development Guide

Welcome to PicoPanda game development! This guide will help you create games using Lua for the PicoPanda handheld.

## Getting Started

### 1. Setup Your Development Environment

#### VS Code (Recommended)
- Install the **PicoPanda VSCode Extension** for graphics editing and export
- `picopanda_api.lua` contains the full API reference with autocomplete support
- Use the extension to create and export graphics binaries

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

-- Current button states
if buttons.up then
    -- Up button is currently held down
end

-- Button press events (triggered once per press)
if buttons.up_pressed then
    -- Up button was just pressed this frame
end
```

**Available buttons:** `up`, `down`, `left`, `right`, `start`, `select`, `a`, `b`

**Button states:**
- `buttons.up` - True while button is held
- `buttons.up_pressed` - True only on the frame when button is first pressed

### Drawing Functions

#### `draw_pixel(x, y, value)`
Draws a single pixel.

```lua
draw_pixel(64, 64, 0x0F)  -- White pixel at center
```

#### `draw_sprite(sprite_size, index, x, y, width, height, flip_x, flip_y)`
Draws a sprite from the sprite sheet.

```lua
-- Draw an 8x8 sprite at position (32, 32)
draw_sprite(PIXELS_8x8, 0, 32, 32, 8, 8, false, false)
```

**Sprite size constants:** `PIXELS_8x8` (currently supported), `PIXELS_16x16`, `PIXELS_32x32` (not yet implemented)

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
Draws text on the screen.

```lua
draw_string(0, 120, "Hello World!", FONT_4X5_FIXED, 1, 0x0F)
```

**Font constants:**
- `FONT_4X5_FIXED` (5) - Default fixed-width font
- `FONT_5X7_FIXED` (3) - Larger fixed-width font
- `FONT_PICOPIXEL` (2) - Pixel art style font

#### `draw_map(celx, cely, sx, sy, celw, celh, layer)`
Draws a region of the tile map to the screen.

```lua
-- Draw a 16x16 tile region at screen position (0, 0)
draw_map(0, 0, 0, 0, 16, 16)
```

#### `get_map_sprite_index(celx, cely)`
Gets the sprite index at a specific map cell.

```lua
local sprite_id = get_map_sprite_index(5, 3)
```

#### `get_sprite_flags(n, f)`
Gets sprite flags for collision detection and game logic.

```lua
local flags = get_sprite_flags(0)  -- Get all flags for sprite 0
local flag1 = get_sprite_flags(0, 1)  -- Get specific flag bit
```

### Camera Functions

#### `set_camera_offset(x, y)`
Sets the camera offset for all future draw operations.

```lua
set_camera_offset(64, 64)  -- Center camera on player
```

#### `get_camera_offset()`
Gets the current camera offset.

```lua
local cam_x, cam_y = get_camera_offset()
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
- **String positioning:** Coordinates represent the bottom-left corner of text

## Graphics Creation

### Using the PicoPanda VSCode Extension

1. **Install the extension** from the VS Code marketplace - Or grab the .vsix from the repo
2. **Create graphics** using the built-in editor
3. **Export graphics binary** (.bin file) containing:
   - Sprite sheet (128x128 pixels, 4-bit greyscale)
   - Tile map (128x64 tiles)
   - Sprite flags (256 sprites, 8 flags each)

### Graphics Binary Structure

The exported graphics binary contains:
- **Sprite Sheet:** 8,192 bytes (128x128 pixels at 4 bits per pixel)
- **Tile Map:** 8,192 bytes (128x64 tiles, 1 byte per tile)
- **Sprite Flags:** 256 bytes (1 byte per sprite, 8 flags per byte)
- **Total:** 16,640 bytes

**Note:** Currently only 8x8 pixel sprites are supported. 16x16 and 32x32 sprite sizes are not yet implemented.

## Building and Uploading

### Complete Build Process

Follow these steps to compile and upload your game to PicoPanda:

#### 1. Create Graphics (VSCode Extension)
- Use the PicoPanda VSCode Extension to create your graphics
- Export as a graphics binary file (e.g., `my_game_graphics.bin`)

#### 2. Build Game Slot Binary
Combine your Lua game code and graphics binary into a single binary:

```bash
cd tools
python make_slot_bin.py --script ../my_game/game.lua --output game_slot.bin --graphics my_game_graphics.bin
```

**Arguments:**
- `--script` or `-s`: Your Lua game file
- `--output` or `-o`: Output binary file
- `--graphics` or `-g`: Graphics binary exported from VSCode extension

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
# 1. Create graphics in VSCode extension and export as graphics.bin

# 2. Build game binary
cd tools
python make_slot_bin.py --script ../my_game/game.lua --output game_slot0.bin --graphics graphics.bin

# 3. Upload to device
python upload_game.py -p /dev/ttyACM0 -b 115200 -f game_slot0.bin
```

### Tool Scripts Reference

All tools are located in the `tools/` folder:

- **`make_slot_bin.py`**: Combines Lua code and graphics binary into game binary
- **`upload_game.py`**: Uploads game binary to PicoPanda via UART
- **`download_game.py`**: Downloads game binary from PicoPanda for verification

Run any script with `-h` for detailed help and usage examples.

## Example Game

Here's a complete working example:

```lua
-- Simple movement example
local player_x = 64
local player_y = 64

function game_logic_init()
    -- Initialize game variables
    player_x = 64
    player_y = 64
end

function game_logic_loop()
    -- Get button input
    local buttons = get_button_status()
    
    -- Handle movement
    if buttons.left_pressed then
        player_x = player_x - 1
    end
    if buttons.right_pressed then
        player_x = player_x + 1
    end
    if buttons.up_pressed then
        player_y = player_y - 1
    end
    if buttons.down_pressed then
        player_y = player_y + 1
    end
    
    -- Keep player on screen
    if player_x < 0 then player_x = 0 end
    if player_x > 127 then player_x = 127 end
    if player_y < 0 then player_y = 0 end
    if player_y > 127 then player_y = 127 end
    
    -- Clear screen
    draw_rectangle(0, 0, 128, 128, true, 0x00)
    
    -- Draw player
    draw_rectangle(player_x, player_y, 8, 8, true, 0x0F)
    
    -- Draw UI
    draw_string(0, 120, "Player: " .. player_x .. "," .. player_y, FONT_4X5_FIXED, 1, 0x0F)
end
```

## Troubleshooting

### Game not working?
1. Check that both `game_logic_init()` and `game_logic_loop()` are defined
2. Verify graphics binary format (16,640 bytes total)
3. Ensure proper button handling (use `_pressed` for single-frame events)
4. Check string positioning (coordinates are bottom-left corner)

### Common Issues
- **Strings off-screen**: Remember that string coordinates represent the bottom-left corner
- **Button not responding**: Use `buttons.button_pressed` for single-press events, `buttons.button` for held state
- **Graphics not showing**: Ensure graphics binary is properly exported from VSCode extension
