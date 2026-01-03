game_title = "Pico8AssetTest_WM"
flip_x = false
flip_y = false
map_x = 0
map_y = 0

function game_logic_init()

end

function game_logic_loop()
    local buttons = get_button_status()

    if(buttons.a_pressed) then
        phrase_play(0)
    end

    if(buttons.b_pressed) then
        phrase_play(1)
    end

    if(buttons.left_pressed) then
        flip_x = true
    end

    if(buttons.right_pressed) then
        flip_x = false
    end

    draw_map(map_x, map_y, map_x*8, map_y*8, 4, 1, 0)
    
    map_x = map_x + 4
    if(map_x > 15) then
        map_x = 0
    end

    map_y = map_y + 1
    if(map_y > 15) then
        map_y = 0
    end
    draw_sprite(PIXELS_8x8, 17, 60, 60, 1, 1, flip_x, flip_y)

    --[[
    x = 0
    y = 0
    for i = 0, 63, 1 do
        draw_sprite(PIXELS_8x8, 17, x, y, 1, 1, flip_x, flip_y)
        x = x + 8
        if(x > 120) then
            x = 0
            y = y + 8
        end
    end
    --]]
end