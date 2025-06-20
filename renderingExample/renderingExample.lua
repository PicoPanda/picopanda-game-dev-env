-- This variable will be global to the script
counter = 0

function game_logic_init()
    print("Lua game_logic_init from C array!")
    counter = 0
end

function game_logic_loop()
    counter = counter + 1
    print("Lua game_logic_loop from C array! Counter:", counter)
    draw_string(0, 10, "Counter: " .. tostring(counter), 5, 1, 0x0F)
    draw_string(0, 20, "Louise is beeldskoon!", 5, 1, 0x0F)
    draw_string(0, 30, "Bevan is n legende!", 5, 1, 0x0F)
end