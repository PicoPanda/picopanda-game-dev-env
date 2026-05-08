game_title = "Lunar Lander"

--game variables
g = 0.0125 --gravity
v_land_max_x = 0.2
v_land_max_y = 0.4
starting_fuel = 300
bonus_fuel = 60

function game_logic_init()
    game_over = false
    round_over = false
    landed = false
    landings = 0
    make_player()
    make_ground()
    make_stars()
    make_vbar()
    make_fuel()
end

function game_logic_loop()
    local buttons = get_button_status()
    if(not round_over) then
        move_player(buttons)
        check_land()
    else
        if(buttons.a) then
            init_player()
            init_ground()
            init_stars()
            if(game_over) then
                fuel.amount = starting_fuel
            elseif(landed) then
                fuel.amount = fuel.amount + bonus_fuel
                if(fuel.amount > starting_fuel) then
                    fuel.amount = starting_fuel
                end
            end
            game_over = false
            round_over = false
            landed = false
        end
    end

    draw_stars()
    draw_ground()
    draw_player()
    draw_vbar()
    draw_fuel()

    if(round_over) then
        if(game_over) then
            draw_string(40, 48, "Game Over", FONT_5X7_FIXED, 1, 0x0E)
            draw_string(40, 60, "Landings: "..landings, FONT_5X7_FIXED, 1, 0x0E)
            draw_string(22, 72, "Press A to play again.", FONT_5X7_FIXED, 1, 0x0E)
        else
            if(landed) then
                draw_string(22, 48, "Successful Landing!", FONT_5X7_FIXED, 1, 0x0E)
                draw_string(44, 60, "+"..bonus_fuel.." Fuel", FONT_5X7_FIXED, 1, 0x0E)
            else
                draw_string(47, 48, "You died!", FONT_5X7_FIXED, 1, 0x0E)
            end
            draw_string(22, 72, "Press A to continue.", FONT_5X7_FIXED, 1, 0x0E)
        end
    end
end

function make_player()
    player = {}
    init_player()
end

function init_player()
    player.x = 60 --position
    player.y = 8
    player.dx = 0 --movement
    player.dy = 0
    player.sprite = 1
    player.thrust = 0.0375
    player.draw_thrust = {u = false, l = false, r = false}
end

function move_player(buttons)
    player.dy = player.dy + g

    thrust(buttons)

    player.x = player.x + player.dx
    player.y = player.y + player.dy

    stay_on_screen()
end

function thrust(buttons)
    player.draw_thrust.u = false
    player.draw_thrust.l = false
    player.draw_thrust.r = false

    if(fuel.amount > 0) then
        local play_sound = false

        --add thrust to movement
        if(buttons.up) then
            player.dy = player.dy - player.thrust
            fuel.amount = fuel.amount - 1
            player.draw_thrust.u = true
            play_sound = true
        end

        if((fuel.amount > 0) and (buttons.left)) then
            player.dx = player.dx - player.thrust
            fuel.amount = fuel.amount - 1
            player.draw_thrust.l = true
            play_sound = true
        end
        if((fuel.amount > 0) and buttons.right) then
            player.dx = player.dx + player.thrust
            fuel.amount = fuel.amount - 1
            player.draw_thrust.r = true
            play_sound = true
        end

        --thrust sound
        if(play_sound) then
            phrase_play(0)
        end
    end
end

function stay_on_screen()
    if(player.x < 0) then
        player.x = 0
        player.dx = 0
    elseif(player.x > 119) then
        player.x = 119
        player.dx = 0
    end

    if(player.y < 0) then
        player.y = 0
        player.dy = 0
    end
end

function draw_player()
    local p_x = math.floor(player.x + 0.5)
    local p_y = math.floor(player.y + 0.5)

    if (round_over and landed) then
        draw_sprite(PIXELS_8x8, player.sprite, p_x, p_y, 1, 1, false, false)
        draw_sprite(PIXELS_8x8, 4, p_x, p_y-8, 1, 1, false, false)
    elseif(round_over) then
        if(exploding_spr <= 9) then
            draw_sprite(PIXELS_8x8, exploding_spr, p_x, p_y, 1, 1, false, false)
            exploding_frc = exploding_frc - 1
            if(exploding_frc == 0) then
                exploding_spr = exploding_spr + 1
                exploding_frc = 10
            end
        end
    else
        draw_sprite(PIXELS_8x8, player.sprite, p_x, p_y, 1, 1, false, false)
        if(player.draw_thrust.l) then
            draw_sprite(PIXELS_8x8, 18, p_x+8, p_y, 1, 1, false, false)
        end
        if(player.draw_thrust.r) then
            draw_sprite(PIXELS_8x8, 16, p_x-8, p_y, 1, 1, false, false)
        end
        if(player.draw_thrust.u) then
            draw_sprite(PIXELS_8x8, 17, p_x, p_y+8, 1, 1, false, false)
        end
    end
end

function make_ground()
    -- Ground
    gnd = {}
    gnd.seg = {}
    gnd.top = 96  --highest point
    gnd.btm = 124 --lowest point

    -- Landing pad.
    pad = {}
    pad.width = 15
    pad.sprite = 2

    init_ground()
end

function init_ground()
    --set up the landing pad
    pad.x = rnd_int(0, 127-pad.width)
    pad.y = rnd_int(gnd.top, gnd.btm);

    if(#gnd.seg > 0) then
        for i in pairs(gnd.seg) do
            gnd.seg[i] = nil
        end
    end

    --create ground at pad
    for i=pad.x,pad.x+pad.width do
        gnd.seg[i] = pad.y
    end

    --create the ground right of pad
    for i=pad.x+pad.width+1,127 do
        local h_l = gnd.seg[i-1]
        local h = rnd_int(h_l-3, h_l+4)
        gnd.seg[i] = clamp_int(h, gnd.top, gnd.btm)
    end

    --create the ground left of pad
    for i=pad.x-1,0,-1 do
        local h_r = gnd.seg[i+1]
        local h = rnd_int(h_r-3, h_r+4)
        gnd.seg[i] = clamp_int(h, gnd.top, gnd.btm)
    end
end

function draw_ground()
    for i=0,127 do
        draw_line(i,gnd.seg[i], i, 127, 3)
    end
    draw_sprite(PIXELS_8x8, pad.sprite, pad.x, pad.y, 2, 1, false, false)
end

function check_land()
    local l_x = math.floor(player.x)     --left side of ship
    local r_x = math.floor(player.x + 7) --right side of ship
    local b_y = math.floor(player.y + 7) --bottom of ship

    over_pad = (l_x >= pad.x) and (r_x <= pad.x + pad.width)
    on_pad = b_y >= pad.y - 1
    slow = (player.dy < v_land_max_y) and (player.dx < v_land_max_x) and (player.dx > -v_land_max_x)

    if(over_pad and on_pad and slow) then
        end_round(true)
    elseif(over_pad and on_pad) then
        end_round(false)
    else
        for i=l_x,r_x do
            if(gnd.seg[i] <= b_y) then
                end_round(false)
            end
        end
    end
end

function end_round(success)
    round_over = true
    if(fuel.amount == 0) then
        game_over = true
    end
    landed = success
    exploding_spr = 5
    exploding_frc = 5

    if(landed) then
        landings = landings + 1
        phrase_play(1, 0)
    else
        phrase_play(2, 0)
    end
end

function make_stars()
    stars = {}
    for i=1,50 do
        local s = {c = 0, x = 0, y = 0}
        table.insert(stars, s)
    end
    init_stars()
end

function init_stars()
    for i=1,50 do
        stars[i].c = rnd_int(0, 14)
        stars[i].x = rnd_int(0, 127)
        stars[i].y = rnd_int(0, 127)
    end
end

function draw_stars()
    for i=1,50 do
        draw_pixel(stars[i].x, stars[i].y, stars[i].c)
    end
end

function make_vbar()
    vbar = {}
    vbar.x_scale = 60
    vbar.y_scale = 30
    vbar.x_pos_centre = 42
    vbar.y_pos_centre = 44
    vbar.x_len_max = 32
    vbar.y_len_max = 32
    vbar.x_lim_p = vbar.x_pos_centre + math.floor(v_land_max_x * vbar.x_scale) - 1
    vbar.x_lim_n = vbar.x_pos_centre - math.floor(v_land_max_x * vbar.x_scale)
    vbar.y_lim_p = vbar.y_pos_centre + math.floor(v_land_max_y * vbar.y_scale) - 1
    vbar.y_lim_n = vbar.y_pos_centre - math.floor(v_land_max_y * vbar.y_scale)
end

function draw_vbar()

    draw_string(0, 6, "v", FONT_5X7_FIXED, 1, 0x0E)
    draw_string(6, 5, "x", FONT_PICOPIXEL, 1, 0x0E)
    draw_string(2, 9, "y", FONT_PICOPIXEL, 1, 0x0E)
    draw_rectangle(vbar.x_pos_centre - 1, 0, 2, 6, false, 0x0E)
    draw_rectangle(0, vbar.y_pos_centre - 1, 6, 2, false, 0x0E)

    draw_line(vbar.x_lim_n, 0, vbar.x_lim_n, 5, 0x0E)
    draw_line(vbar.x_lim_p, 0, vbar.x_lim_p, 5, 0x0E)
    draw_line(0, vbar.y_lim_n, 5, vbar.y_lim_n, 0x0E)
    draw_line(0, vbar.y_lim_p, 5, vbar.y_lim_p, 0x0E)

    local vx = math.floor(player.dx * vbar.x_scale)
    vx = clamp_int(vx, -vbar.x_len_max, vbar.x_len_max)
    local vy = math.floor(player.dy * vbar.y_scale)
    vy = clamp_int(vy, -vbar.y_len_max, vbar.y_len_max)
    local x
    local y

    --[[
    draw_string(2, 6, "vx: "..vx, FONT_PICOPIXEL, 1, 0x0E)
    draw_string(2, 12, "vy: "..vy, FONT_PICOPIXEL, 1, 0x0E)
    --]]

    if(vx >= 0) then
        x = vbar.x_pos_centre
    else
        x = vbar.x_pos_centre + vx
        vx = math.abs(vx)
        --[[
            TODO: There is a but in the draw function that doesn't draw if x or y is negative, fix this.
            It should be able to draw off of screen.
        --]]
        if(x < 0) then
            x = 0
        end
    end
    draw_rectangle(x, 2, vx, 2, false, 0x0A)
    --[[
        TODO: There seems to be a bug with draw_rectangle, if the width is 0 then it draws a width of 2 in reverse.
    --]]

    if(vy >= 0) then
        y = vbar.y_pos_centre
    else
        y = vbar.y_pos_centre + vy
        vy = math.abs(vy)
        --[[
            TODO: There is a but in the draw function that doesn't draw if x or y is negative, fix this.
            It should be able to draw off of screen.
        --]]
        if(y < 0) then
            y = 0
        end
    end
    draw_rectangle(2, y, 2, vy, false, 0x0A)
end

function make_fuel()
    fuel = {}
    fuel.scale = 10
    fuel.amount = starting_fuel
    local bar_len = math.floor(fuel.amount / fuel.scale)
    fuel.ibar = {x = 127 - bar_len, y = 1, h = 6, l = bar_len, c = 1}
    fuel.obar = {x = (fuel.ibar.x - 1), y = (fuel.ibar.y - 1), h = (fuel.ibar.h + 2), l = (fuel.ibar.l + 2), c = 10}
end

function draw_fuel()
    draw_rectangle(fuel.obar.x, fuel.obar.y, fuel.obar.l, fuel.obar.h, true, fuel.obar.c)
    local bar_len = math.floor(fuel.amount / fuel.scale)
    draw_rectangle(fuel.ibar.x, fuel.ibar.y, bar_len, fuel.ibar.h, true, fuel.ibar.c)
end