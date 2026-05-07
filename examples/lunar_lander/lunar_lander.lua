game_title = "Lunar Lander"

--game variables
g = 0.0125 --gravity
v_land_max_x = 0.2
v_land_max_y = 0.4

function game_logic_init()
    game_over=false
    win=false
    make_player()
    make_ground()
    make_stars()
    make_vbar()
end

function game_logic_loop()
    local buttons = get_button_status()
    if(not game_over) then
        move_player(buttons)
        check_land()
    else
        if(buttons.a) then
            game_logic_init()
        end
    end

    draw_stars()
    draw_ground()
    draw_player(buttons)
    draw_vbar()

    if(game_over) then
        if(win) then
            draw_string(48, 48, "You win!", FONT_5X7_FIXED, 1, 0x0E)
        else
            draw_string(47, 48, "You died!", FONT_5X7_FIXED, 1, 0x0E)
        end
        draw_string(20, 60, "Press A to play again.", FONT_5X7_FIXED, 1, 0x0E)
    end
end

function make_player()
    player = {}
    player.x = 60 --position
    player.y = 8
    player.dx = 0 --movement
    player.dy = 0
    player.sprite = 1
    player.alive = true
    player.thrust = 0.0375
end

function move_player(buttons)
    player.dy = player.dy + g

    thrust(buttons)

    player.x = player.x + player.dx
    player.y = player.y + player.dy

    stay_on_screen()
end

function thrust(buttons)
    --add thrust to movement
    if(buttons.left) then
        player.dx = player.dx - player.thrust
    end
    if(buttons.right) then
        player.dx = player.dx + player.thrust
    end
    if(buttons.up) then
        player.dy = player.dy - player.thrust
    end

    --thrust sound
    if(buttons.left or buttons.right or buttons.up) then
        phrase_play(0)
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

function draw_player(buttons)
    local p_x = math.floor(player.x + 0.5)
    local p_y = math.floor(player.y + 0.5)

    if (game_over and win) then
        draw_sprite(PIXELS_8x8, player.sprite, p_x, p_y, 1, 1, false, false)
        draw_sprite(PIXELS_8x8, 4, p_x, p_y-8, 1, 1, false, false)
    elseif(game_over) then
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
        if(buttons.left) then
            draw_sprite(PIXELS_8x8, 18, p_x+8, p_y, 1, 1, false, false)
        end
        if(buttons.right) then
            draw_sprite(PIXELS_8x8, 16, p_x-8, p_y, 1, 1, false, false)
        end
        if(buttons.up) then
            draw_sprite(PIXELS_8x8, 17, p_x, p_y+8, 1, 1, false, false)
        end
    end
end



function make_ground()
    --create the ground
    gnd = {}
    local top = 96  --highest point
    local btm = 124 --lowest point

    --set up the landing pad
    pad = {}
    pad.width = 15
    pad.x = rnd_int(0, 127-pad.width)
    pad.y = rnd_int(top, btm);
    pad.sprite = 2

    --create ground at pad
    for i=pad.x,pad.x+pad.width do
        gnd[i] = pad.y
    end

    --create the ground right of pad
    for i=pad.x+pad.width+1,127 do
        local h_l = gnd[i-1]
        local h = rnd_int(h_l-3, h_l+4)
        gnd[i] = clamp_int(h, top, btm)
    end

    --create the ground left of pad
    for i=pad.x-1,0,-1 do
        local h_r = gnd[i+1]
        local h = rnd_int(h_r-3, h_r+4)
        gnd[i] = clamp_int(h, top, btm)
    end
end

function draw_ground()
    for i=0,127 do
        draw_line(i,gnd[i], i, 127, 3)
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
        end_game(true)
    elseif(over_pad and on_pad) then
        end_game(false)
    else
        for i=l_x,r_x do
            if(gnd[i] <= b_y) then
                end_game(false)
            end
        end
    end
end

function end_game(won)
    game_over = true
    win = won
    exploding_spr = 5
    exploding_frc = 5

    if(win) then
        phrase_play(1, 0)
    else
        phrase_play(2, 0)
    end
end

function make_stars()
    stars = {}
    for i=1,50 do
        local s = {}
        s.c = rnd_int(0, 14)
        s.x = rnd_int(0, 127)
        s.y = rnd_int(0, 127)
        table.insert(stars, s)
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
    vbar.y_scale = 40
    vbar.x_lim_p = 64 + math.floor(v_land_max_x * vbar.x_scale) - 1
    vbar.x_lim_n = 63 - math.floor(v_land_max_x * vbar.x_scale) + 1
    vbar.y_lim_p = 64 + math.floor(v_land_max_y * vbar.y_scale) - 1
    vbar.y_lim_n = 63 - math.floor(v_land_max_y * vbar.y_scale) + 1
end

function draw_vbar()
    draw_rectangle(63, 0, 2, 6, false, 0x0E)
    draw_rectangle(0, 63, 6, 2, false, 0x0E)

    draw_line(vbar.x_lim_n, 0, vbar.x_lim_n, 5, 0x0E)
    draw_line(vbar.x_lim_p, 0, vbar.x_lim_p, 5, 0x0E)
    draw_line(0, vbar.y_lim_n, 5, vbar.y_lim_n, 0x0E)
    draw_line(0, vbar.y_lim_p, 5, vbar.y_lim_p, 0x0E)

    local vx = math.floor(player.dx * vbar.x_scale)
    local vy = math.floor(player.dy * vbar.y_scale)
    local x
    local y

    --[[
    draw_string(2, 6, "vx: "..vx, FONT_PICOPIXEL, 1, 0x0E)
    draw_string(2, 12, "vy: "..vy, FONT_PICOPIXEL, 1, 0x0E)
    --]]

    if(vx >= 0) then
        x = 64
    else
        x = 64 + vx
        vx = math.abs(vx)
        --[[
            TODO: There is a but in the draw function that doesn't draw if x or y is negative, fix this.
            It should be able to draw off of screen.
        --]]
        if(x < 0) then
            x = 0
        end
    end
    if(vx > 64) then vx = 64 end
    draw_rectangle(x, 2, vx, 2, false, 0x0A)
    --[[
        TODO: There seems to be a bug with draw_rectangle, if the width is 0 then it draws a width of 2 in reverse.
    --]]

    if(vy >= 0) then
        y = 64
    else
        y = 64 + vy
        vy = math.abs(vy)
        --[[
            TODO: There is a but in the draw function that doesn't draw if x or y is negative, fix this.
            It should be able to draw off of screen.
        --]]
        if(y < 0) then
            y = 0
        end
    end
    if(vy > 64) then vy = 64 end
    draw_rectangle(2, y, 2, vy, false, 0x0A)
end