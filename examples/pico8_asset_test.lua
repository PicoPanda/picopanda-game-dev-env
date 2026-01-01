flip_x = false
flip_y = false

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

    draw_map(0, 0, 0, 0, 16, 16, 0)
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