game_title = "Lunar Lander"

--game variables
g = 0.0125 --gravity

function game_logic_init()
    game_over=false
    win=false
    make_player()
    make_ground()
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

    draw_ground()
    draw_player(buttons)
    if(game_over) then
        if(win) then
            draw_string(48, 48, "you win!", FONT_5X7_FIXED, 1, 0x0E)
        else
            draw_string(47, 48, "you died!", FONT_5X7_FIXED, 1, 0x0E)
        end
        draw_string(20, 70, "press A to play again", FONT_5X7_FIXED, 1, 0x0E)
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
                exploding_frc = 5
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
    local btm = 120 --lowest point

    --set up the landing pad
    pad = {}
    pad.width = 15
    pad.x = 12
    pad.y = 100
    pad.sprite = 2

    --create ground at pad
    for i=pad.x,pad.x+pad.width do
        gnd[i] = pad.y
    end

    --create the ground right of pad
    for i=pad.x+pad.width+1,127 do
        gnd[i] = 100
    end

    --create the ground left of pad
    for i=pad.x-1,0,-1 do
        gnd[i] = 100
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
    slow = (player.dy < 0.5) and (player.dy < 0.25)

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