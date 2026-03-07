function game_logic_init()

end

function game_logic_loop()
    local buttons = get_button_status()

    if(buttons.a_pressed) then
        phrase_play(0)
    end

    if(buttons.b_pressed) then
        phrase_stop(-1)
    end

    draw_string(10, 60, "Audio Test: A to play, B to Stop", FONT_4X5_FIXED, 1, 0x0F)
end
