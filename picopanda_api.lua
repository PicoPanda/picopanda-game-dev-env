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