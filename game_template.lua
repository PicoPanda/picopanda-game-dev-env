-- PicoPanda Game Template

-- Game variables
local player_x = 64
local player_y = 64
local score = 0

-- Game initialization
function game_logic_init()
    -- Initialize your game here
    player_x = 64
    player_y = 64
    score = 0
end

-- Main game loop (called every frame at 60 FPS)
function game_logic_loop()
    -- Get button input
    local buttons = get_button_status()

    -- Handle input
    if buttons.left and player_x > 0 then
        player_x = player_x - 1
    end
    if buttons.right and player_x < 127 then
        player_x = player_x + 1
    end
    if buttons.up and player_y > 0 then
        player_y = player_y - 1
    end
    if buttons.down and player_y < 127 then
        player_y = player_y + 1
    end

    -- Clear screen (draw black background)
    draw_rectangle(0, 0, 128, 128, true, 0x00)

    -- Draw player (example using a 16x16 sprite)
    draw_sprite(PIXELS_16x16, 0, player_x, player_y, 16, 16, false, false)

    -- Draw UI
    draw_string(0, 0, "Score: " .. tostring(score), FONT_5X7_FIXED, 1, 0x0F)
    draw_string(0, 10, "Pos: " .. player_x .. "," .. player_y, FONT_5X7_FIXED, 1, 0x0F)

    -- Example: Draw some shapes
    draw_circle(32, 32, 8, true, 0x0E)  -- Filled circle
    draw_rectangle(100, 100, 20, 20, false, 0x0D)  -- Outline rectangle

    -- Example: Draw a line
    draw_line(0, 127, 127, 0, 0x0C)
end