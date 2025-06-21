counter = 0

function game_logic_init()
    counter = 0
end

function game_logic_loop()
    counter = counter + 1

    local buttons = get_button_status()

    if buttons.up then
        draw_string(0, 80, "UP pressed!", 5, 1, 0x0F)
    end
    
    draw_string(0, 10, "Counter: " .. tostring(counter), 5, 1, 0x0F)
    draw_pixel(30, 30, 0x0F);
    
    draw_circle(63, 63, 15, true, 0x0F);

    draw_line(0, 0, 127, 127, 0x0F);

    draw_rectangle(0, 63, 10, 10, true, 0x0F);

    draw_sprite( 32, 0, 32, 32, 2, 2, false, false)

end