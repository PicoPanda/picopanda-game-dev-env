---@meta

-- PicoPanda Game Engine API
-- This file provides autocomplete and documentation for the PicoPanda Lua API
-- Include this file in your Lua projects for better development experience

---@class ButtonStatus
---@field up boolean True if the UP button is pressed
---@field down boolean True if the DOWN button is pressed
---@field left boolean True if the LEFT button is pressed
---@field right boolean True if the RIGHT button is pressed
---@field start boolean True if the START button is pressed
---@field select boolean True if the SELECT button is pressed
---@field a boolean True if the A button is pressed
---@field b boolean True if the B button is pressed
---@field up_pressed boolean True if the UP button was pressed in the last frame
---@field down_pressed boolean True if the DOWN button was pressed in the last frame
---@field left_pressed boolean True if the LEFT button was pressed in the last frame
---@field right_pressed boolean True if the RIGHT button was pressed in the last frame
---@field start_pressed boolean True if the START button was pressed in the last frame
---@field select_pressed boolean True if the SELECT button was pressed in the last frame
---@field a_pressed boolean True if the A button was pressed in the last frame
---@field b_pressed boolean True if the B button was pressed in the last frame

---@class SpriteSize
---@field PIXELS_8x8 number 8x8 pixel sprites
---@field PIXELS_16x16 number 16x16 pixel sprites
---@field PIXELS_32x32 number 32x32 pixel sprites

-- Sprite size constants
PIXELS_8x8 = 8
PIXELS_16x16 = 16
PIXELS_32x32 = 32

-- Font constants
FONT_ORG_01 = 0
FONT_FREE_MONO_9PT_7B = 1
FONT_PICOPIXEL = 2
FONT_5X7_FIXED = 3
FONT_FREE_SERIF_9PT_7B = 4
FONT_4X5_FIXED = 5

---Get the current status of all buttons
---@return ButtonStatus A table containing the state of all buttons
function get_button_status() end

---Draw a single pixel on the screen
---@param x number X coordinate (0-127)
---@param y number Y coordinate (0-127)
---@param value number Pixel value (0-15)
function draw_pixel(x, y, value) end

---Draw a sprite from the sprite sheet
---@param sprite_size number Size of sprites in the sheet (PIXELS_8x8, PIXELS_16x16, PIXELS_32x32)
---@param index number Sprite index in the sheet
---@param coord_x number X coordinate to draw at
---@param coord_y number Y coordinate to draw at
---@param width number Width of the sprite to draw
---@param height number Height of the sprite to draw
---@param flip_x boolean Flip sprite horizontally
---@param flip_y boolean Flip sprite vertically
function draw_sprite(sprite_size, index, coord_x, coord_y, width, height, flip_x, flip_y) end

---Draw a line between two points
---@param x1 number Start X coordinate
---@param y1 number Start Y coordinate
---@param x2 number End X coordinate
---@param y2 number End Y coordinate
---@param value number Line color value (0-15)
function draw_line(x1, y1, x2, y2, value) end

---Draw a circle
---@param x_center number Center X coordinate
---@param y_center number Center Y coordinate
---@param radius number Circle radius
---@param filled boolean True to draw filled circle, false for outline
---@param value number Circle color value (0-15)
function draw_circle(x_center, y_center, radius, filled, value) end

---Draw a rectangle
---@param x1 number Top-left X coordinate
---@param y1 number Top-left Y coordinate
---@param width number Rectangle width
---@param height number Rectangle height
---@param filled boolean True to draw filled rectangle, false for outline
---@param value number Rectangle color value (0-15)
function draw_rectangle(x1, y1, width, height, filled, value) end

---Draw text on the screen
---@param x number X coordinate
---@param y number Y coordinate
---@param str string Text to draw
---@param font_index number Font index (5 for default font)
---@param scale_factor number Text scale factor
---@param value number Text color value (0-15)
function draw_string(x, y, str, font_index, scale_factor, value) end

---Draw a region of the map to the screen, using sprite sheet and flags
---@param celx number The column of the map cell in the upper left corner (0 = leftmost)
---@param cely number The row of the map cell in the upper left corner (0 = topmost)
---@param sx number The x coordinate on the screen to place the upper left corner
---@param sy number The y coordinate on the screen to place the upper left corner
---@param celw number The number of map cells wide in the region to draw
---@param celh number The number of map cells tall in the region to draw
---@param layer number|nil If specified, only draw sprites that have flags set for every bit in this value (bitfield). Default is 0 (draw all sprites).
function draw_map(celx, cely, sx, sy, celw, celh, layer) end

---Get the sprite index assigned to a map cell
---@param celx number The column (x) coordinate of the map cell
---@param cely number The row (y) coordinate of the map cell
---@return number The sprite index at that cell (0-255), or 255 if out of bounds
function get_map_sprite_index(celx, cely) end

---Get the value of a sprite's flags
---@param n number The sprite number (0-255)
---@param f number|nil The flag index (1-8). If 0 or omitted, returns the full flag byte. If 1-8, returns 1 if that flag bit is set, else 0.
---@return number The flag value or bit
function get_sprite_flags(n, f) end

---Set the camera offset for all future draw operations
---@param x number The x pixel offset to subtract from draw coordinates
---@param y number The y pixel offset to subtract from draw coordinates
function set_camera_offset(x, y) end

---Get the current camera offset
---@return number x The current x pixel offset
---@return number y The current y pixel offset
function get_camera_offset() end

--- Play a phrase
--- @param index number         The index of the phrase to play
--- @param channel number       The channel on which to play the phrase (optional).
---                             Selects the next available channel if omitted or
---                             negative.
function phrase_play() end

--- Stop a phrase
--- @param index number         The index of the phrase to stop. Pass a negative
---                             number to disregard phrase and just stop the selected
---                             audio channel(s).
--- @param channel number       The channel on which to stop the phrase. All channels
---                             if omitted or negative.
function phrase_stop() end

--- Returns a random integer from a specified range.
--- If both bounds are provided, returns an integer such that:
---     lower <= n < upper
--- 
--- If only one argument is provided, it is treated as the upper bound and the
--- returned integer is:
---     0 <= n < upper
--- @param[opt] lower number    The inclusive lower bound.
--- @param upper number         The exclusive upper bound.
--- @return number n            A random integer within the specified range.
function rnd_int([lower,] upper) end

--- Returns the middle value of 3 given values.
--- @param a number             The first value.
---                             Values in the range of int32_t are allowed.
--- @param b number             The second value.
---                             Values in the range of int32_t are allowed.
--- @param c number             The third value.
---                             Values in the range of int32_t are allowed.
--- @return number n            The value middle value
function mid_int(a, b, c) end

--- Clamps an integer to within a specified range and returns the clamped value
--- and a boolean specifying whether clamping was applied.
---     lower <= n <= upper
---     clamped = (boolean)(n <= lower) or (boolean)(n >= upper)
--- @param val number           The value to clamp.
---                             Values in the range of int32_t are allowed.
--- @param lower number         The inclusive lower value of the clamping interval.
---                             Values in the range of int32_t are allowed.
--- @param upper number         The inclusive upper value of the clamping interval.
---                             Values in the range of int32_t are allowed.
--- @return number n            The value after clamping has been applied.
--- @return boolean clamped     A boolean specifying whether clamping was necessary.
function clamp_int(val, lower, upper) end

-- Game lifecycle functions (these should be defined in your game script)

---Called once when the game starts
---Use this for initialization
function game_logic_init() end

---Called every frame (60 FPS)
---Use this for game logic and rendering
function game_logic_loop() end

-- Example usage:
--[[
function game_logic_init()
    -- Initialize your game here
    player_x = 64
    player_y = 64
end

function game_logic_loop()
    -- Get button input
    local buttons = get_button_status()
    
    -- Handle input
    if buttons.left then
        player_x = player_x - 1
    end
    if buttons.right then
        player_x = player_x + 1
    end
    
    -- Clear screen (draw black background)
    draw_rectangle(0, 0, 128, 128, true, 0x00)
    
    -- Draw player
    draw_sprite(16, 0, player_x, player_y, 16, 16, false, false)
    
    -- Draw UI
    draw_string(0, 0, "Score: 100", 5, 1, 0x0F)
end
--]] 