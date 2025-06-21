Counter = 0
Flip = false

function game_logic_init()
    Counter = 0
    Flip = false
end

function game_logic_loop()
    Counter = Counter + 1

    local buttons = get_button_status()

    if buttons.up then
        draw_string(0, 80, "UP pressed!", FONT_4X5_FIXED, 1, 0x0F)
    end

    draw_string(0, 10, "Counter: " .. tostring(Counter), 5, 1, 0x0F)
    draw_pixel(30, 30, 0x0F);

    draw_circle(63, 63, 15, true, 0x0F);

    draw_line(0, 0, 127, 127, 0x0F);

    draw_rectangle(0, 63, 10, 10, true, 0x0F);

    if Counter % 100 == 0 then
        Flip = not Flip

    end

    draw_sprite(PIXELS_32x32, 0, 32, 32, 2, 2, Flip, false)

end