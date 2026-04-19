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

### Audio Functions

####  `phrase_play(index, channel)`
Plays a phrase.<br>
The channel parameter is optional, if it is omitted or is negative then an available
channel is selected.

```lua
phrase_play(1) -- Play phrase 1 on an available channel.

phrase_play(11, 3) -- Play phrase on channel 3.
```

####  `phrase_stop(index, channel)`
Stops a phrase.<br>
The index parameter can be negative, which causes any phrase on the selected channel
stopped
The channel parameter is optional, if it is omitted or is negative then the phrase
is stopped on all channels on which it is being played.<br>


```lua
phrase_stop(1) -- Stop phrase 1 on all channels which are currently playing it.

phrase_stop(11, 3) -- Stop phrase 11 on channel 3. Only effective if phrase 11 is currently being played on channel 3.

phrase_stop(-1, 3) -- Stop audio on channel 3.

phrase_stop(-1, -1) -- Stop audio on all channels.

```

### Math Functions

#### `rnd_int([lower,] upper)`
Returns a random integer greater than or equal to the lower bound and less than
the upper bound. If only one argument is given then the argument is taken as the
upper bound and the lower bound is taken as 0. Arguments can be in the range of
a signed 32-bit integer. Return value is in the range of a signed 32-bit integer.

```lua
x = rnd_int(100) -- Returns a value which could be any value from 0 to 99.

x = rnd_int(1000, 3001) -- Returns a value which could be any value from 1000 to 3000.

```

#### `mid_int(a, b, c)`
Returns the middle value of 3 given values. Arguments can be in the range of a
signed 32-bit integer. Return value is in the range of a signed 32-bit integer.

```lua
x = mid_int(1, 3, 4) -- Returns 2.

x = mid_int(10, 100, 1000) -- Returns 100.

x = mid_int(10, 10, 1000) -- Returns 10.

x = mid_int(10, 1000, 1000) -- Returns 1000.

```

#### `clamp_int(val, lower, upper)`
Clamps an integer to within a specified range and returns the clamped value and
a boolean specifying whether clamping was applied. the lower and upper bounds are
both inclusive. Arguments can be in the range of a signed 32-bit integer. Return
value is in the range of a signed 32-bit integer.

```lua
x, b = clamp_int(5, 0, 10) -- Returns 5 and false.

x, b = clamp_int(15, 0, 10) -- Returns 15 and true.

x, b = clamp_int(-5, 0, 10) -- Returns 0 and true.

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
- `0x0F` - Pure White (Currently used as the transparent colour)

## Display Specifications

- **Resolution:** 128x128 pixels
- **Color depth:** 4-bit greyscale (16 shades)
- **Frame rate:** 60 FPS
- **Coordinate system:** (0,0) at top-left, (127,127) at bottom-right
- **String positioning:** Coordinates represent the bottom-left corner of text

## Graphics

### Graphics Capabilities
- Sprite sheet (128x128 pixels, 4-bit greyscale)
- Sprite flags (256 sprites, 8 flags each)
- Tile map (128x64 tiles)

### Graphics Binary Structure

PicoPand stores the graphics in a game binary as follows:
- **Sprite Sheet:** 8,192 bytes (128x128 pixels at 4 bits per pixel)
- **Tile Map:** 8,192 bytes (128x64 tiles, 1 byte per tile)
- **Sprite Flags:** 256 bytes (1 byte per sprite, 8 flags per byte)
- **Total:** 16,640 bytes

### PICO-8 Editor

The current recommended method for creating all the graphics assets is with the
PICO-8 sprite editor and the PICO-8 map editor. The PICO-8 palette is changed into
greyscale as follows:
- PICO-8 index 0, which is black, maps to PicoPanda index 15 and is used for transparency.
- PICO-8 index 5, which is a dark grey, maps to PicoPanda index 0 which is black.
- All other colours map to greyscale in order of colour luminosity. This works surprisingly
  well in most cases.

Once the graphics have been created, use the *pico8_asset_converter.py* script to
extract it. From the root directory of the repo, the command will look like this:

```bash
python ./tools/pic8_asset_converter/pico8_asset_converter.py --input path/to/my_pico8_file.p8 --gfx
```

or on windows

```powershell
python .\\tools\\pic8_asset_converter\\pico8_asset_converter.py --input path\\to\\my_pico8_file.p8 --sgfx
```

The script will then generate a file named *my_pico8_file_pp_graphics.p8* containing
the sprites, sprite flags and the map in the required binary format. This binary
filr can then be passed in to the *make_slot_bin.py* script with the *--graphics*
option. See the [Building and Uploading](#building-and-uploading) section.

### Using the PicoPanda VSCode Extension

1. **Install the extension** from the VS Code marketplace - Or grab the .vsix from the repo
2. **Create graphics** using the built-in editor
3. **Export graphics binary** (.bin file) which contains the graphics packed into a suitable binary structure.

**Note:** Currently only 8x8 pixel sprites are supported. 16x16 and 32x32 sprite sizes are not yet implemented.

## Audio

### Audio Capabilities
Currently PicoPanda supports playback of phrases. A phrase consists of the following:
- 32 notes, each represented by a 32 bit integer of which the fields are ase follows:
    - **note[7:0]:** Reserved for future use
    - **note[11:8]:** Effect
    - **note[15:12]:** Right Volume
    - **note[19:16]:** Left Volume
    - **note[23:20]:** Waveform (instrument)
    - **note[27:24]:** Octave
    - **note[31:28]:** Note
- An 8-bit ticksPerNote value which sets the duration for the notes of the phrase.
Tick duration is 8ms. Therefore, if the ticksPerNote value of the phrase is set
to 50, then each note in the phrase will be played for 400ms.
- An 8-bit loopStart index which sets the note index within the phrase at which
looping of the phrase must start.
- An 8-bit loopEnd index which sets the note index within the phrase at which
looping of the phrase must End.

**Note:** Allowance is made for 256 phrases. The idea is to have a fixed note storage
of 8kB, but then to allow some sort of configuration for phrase length. One can then
decide to have 64 phrases of 32 notes each, 128 phrases of 16 notes each or 256
phrases of 8 notes each. Or even split the note storage into sections with each
section containing a different phrase length. Bottom line is, 256 indexes of phrase
data will be enough.

### Audio Binary Format
The game engine expects the audio information to be in the following binary format:
- **Note Data:** 8,192 bytes of note data arranged in 32 bit integers starting with
note 0 of phrase 0 and ending with the last note of the last phrase. All notes and
all phrases must be populated in the binary regardless of use.
- **Phrase Data:** 768 bytes containing ticksPerNote, loopStart and loopEnd values
for each phrase starting with ticksPerNote for phrase 0 and ending with loopEnd
of the last note. That is, the first 3 bytes of the binary section contains ticksPerNote,
loopStart and loopEnd for phrase 0.
- **Current Total:** 8960 bytes.

### Audio Creation
Currently the only intuitive method of creating audio is to create the audio phrases
with the SFX editor in PICO-8 fantasy console and then to convert them to the binary
format expected by PicoPanda with the *pico8_asset_converter.py* script. Each PICO-8
SFX corresponds to a PicoPanda Phrase. Not all PICO-8 functionality is supported yet,
the tables below show how PICO-8 SFX values map to PicoPanda phrase values.

#### Notes

| Pico8 Note | PicoPanda Note | PicoPanda Value |
|----|----|----|
| C  | C  | 0  |
| C# | C# | 1  |
| D  | D  | 2  |
| D# | D# | 3  |
| E  | E  | 4  |
| F  | F  | 5  |
| F# | F# | 6  |
| G  | G  | 7  |
| G# | G# | 8  |
| A  | A  | 9  |
| A# | A# | 10 |
| B  | B  | 11 |

#### Octaves

| Pico8 Octave | PicoPanda Octave | PicoPanda Value |
|----|------|------|
|    | 0    | 0    |
|    | 1    | 1    |
| 0  | 2    | 2    |
| 1  | 3    | 3    |
| 2  | 4    | 4    |
| 3  | 5    | 5    |
| 4  | 6    | 6    |
| 5  | None | None |

**Note:** Octaves 0 and 1 are available in PicoPanda, but the are not recommended for use.

### Volume

| Pico8 Volume | PicoPanda Volume | 
|----|----|
| 0  | 0  |
| 1  | 1  |
| 2  | 3  |
| 3  | 4  |
| 4  | 6  |
| 5  | 7  |
| 6  | 9  |
| 7  | 10 |

#### Instruments

| Pico8 Instrument | Pico8 Value | PicoPanda Waveform | PicoPanda Value |
|------------|----|------------------|----|
| Triangle   | 0  | Triangle         | 2  |
| Tilted Saw | 1  | Tilted Saw       | 3  |
| Saw        | 2  | Straight Saw     | 4  |
| Square     | 3  | Square           | 0  |
| Pulse      | 4  | PulSe            | 1  |
| Organ      | 5  | Organ            | 6  |
| Noise      | 6  | Random Bit Noise | 9  |
| Phaser     | 7  | Sin              | 5  |
|            |    | White Noise Lin  | 7  |
|            |    | White Noise Hyp  | 8  |
|            |    | Silence          | 10 |

#### Effects

| Pico8 Effect | Pico8 Value | PicoPanda Effect | PicoPanda Value |
|---------------|---|----------|---|
| None          | 0 | None     | 0 |
| Slide         | 1 | None     | 0 |
| Vibrato       | 2 | None     | 0 |
| Drop          | 3 | None     | 0 |
| Fade In       | 4 | Fade In  | 1 |
| Fade Out      | 5 | Fade Out | 2 |
| Arpeggio Fast | 6 | None     | 0 |
| Arpeggio Slow | 7 | None     | 0 |

### Audio Conversion
Use the *pico8_asset_converter.py* script to extract the audio. From the root directory
of the repo, the command will look like this:

```bash
python ./tools/pic8_asset_converter/pico8_asset_converter.py --input path/to/my_pico8_file.p8 --sfx
```

or on windows

```powershell
python .\\tools\\pic8_asset_converter\\pico8_asset_converter.py --input path\\to\\my_pico8_file.p8 --sfx
```

The script will then generate a file named *my_pico8_file_pp_audio.p8* which can be
passed in to the *make_slot_bin.p8* script with the *--audio* option.

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
python make_slot_bin.py --script ../my_game/game.lua --output game_slot.bin --graphics my_game_graphics.bin --audio my_pico8_file_pp_audio.p8
```

**Arguments:**
- `--script` or `-s`: Your Lua game file
- `--output` or `-o`: Output binary file
- `--graphics` or `-g`: Graphics binary exported from VSCode extension
- `--audio` or `-a`: Audio binary file

#### 3. Upload to PicoPanda
Upload the game binary to your PicoPanda device:

```bash
python upload_game.py -p /dev/ttyACM0 -b 115200 -f game_slot.bin
```

**Arguments:**
- `-p /dev/ttyACM0`: Serial port (adjust for your system)
- `-b 115200`: Baud rate
- `-f game_slot.bin`: Binary file to upload

### Testing in the Emulator

Once you've created your `game_slot.bin` file, you can test it in the PicoPanda emulator before uploading to the physical device:

1. **Start the PicoPanda emulator**
2. **Select a game slot** (e.g., Slot 0, Slot 1, etc.)
3. **Drag and drop** your `game_slot.bin` file onto the emulator window
4. **The game will automatically load and run**

This allows you to quickly test your game logic, graphics, and gameplay without needing to upload to the physical device each time you make changes.

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
