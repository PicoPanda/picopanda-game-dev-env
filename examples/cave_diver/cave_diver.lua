game_title = "Cave Diver"

--game variables
gravity = 0.065

function game_logic_init()
    player_died = true
    game_over = false
    start_pause = 60
    level_inc = 180
    level_count = level_inc
    roof_level_min = 33
    roof_level_max = 38
    floor_level_min = 94
    floor_level_max = 89
    roof_max_level = false
    floor_max_level = false
    change_offset = false
    offset_inc = 10
    offset_count = offset_inc
    make_bubbles()
    make_cave()
    make_player()
end

function game_logic_loop()

    -- Update
    local buttons = get_button_status()
    
    if(start_pause > 0) then
        start_pause = start_pause - 1
    else
        if(not game_over) then
            update_level()
            update_bubbles()
            update_cave()
            move_player(buttons)
            check_hit()
        else
            if(buttons.a) then
                game_logic_init() --restart
            end
        end
    end

    -- Draw
    if(game_over) then
        draw_cave()
        draw_player()
        draw_string(40, 44, "Game Over!", FONT_5X7_FIXED, 1, 0x0E)
        score_string = "Your Score: "..player.score
        draw_string(26, 54, score_string, FONT_5X7_FIXED, 1, 0x0E)
        draw_string(20, 64, "Press A to restart.", FONT_5X7_FIXED, 1, 0x0E)
    else
        draw_bubbles(0)
        draw_cave()
        draw_player()
        draw_bubbles(1)
        score_string = "Score: "..player.score
        draw_string(2, 8, score_string, FONT_5X7_FIXED, 1, 0x0E)
        if(start_pause > 0) then
            draw_string(24, 44, "Press UP to swim.", FONT_5X7_FIXED, 1, 0x0E)
        end
    end
end


--> Player

function make_player()
    player={}
    player.x=24    -- Position
    player.y=60
    player.dy=0    -- Sink speed
    player.sprite=1
    player.speed=1 -- Swim speed
    player.score=0
    player.dead=false
end

function draw_player()
    if(player.dead) then
        player.sprite=3
    elseif(player.dy<0) then
        player.sprite=1
    else
        player.sprite=2
    end

    local p_x = math.floor(player.x + 0.5)
    local p_y = math.floor(player.y)
    draw_sprite(PIXELS_8x8, player.sprite, p_x, p_y, 1, 1, false, false)
end

function move_player(buttons)
    player.dy = player.dy + gravity

    -- Thrust up
    if(not player.dead and buttons.up_pressed) then
        player.dy = player.dy - 3
        phrase_play(0)
    end

    -- Move to new position
    player.y = player.y + player.dy

    -- Update score
    player.score = player.score + player.speed
end

function check_hit()
    for i=player.x,player.x+1 do
        if(not player.dead and cave.seg[i+1].top > player.y) then
            player.dead=true
            player.dy=0
            phrase_play(2)
            if(player.y<cave.seg[i+1].top) then
                player.y=cave.seg[i+1].top
                break
            end
        elseif(cave.seg[i+1].bot<player.y+7) then
            player.dead=true
            game_over=true
            phrase_play(1)
            if(player.y+7>cave.seg[i+1].bot) then
                player.y=cave.seg[i+1].bot-7
                break
            end
        end
    end
end

function update_level()
    level_count = level_count - 1
    if(level_count == 0) then
        level_count = level_inc

        if(cave.top_lim_l < roof_level_max) then
            cave.top_lim_l = cave.top_lim_l + 1
        else
            roof_max_level = true
        end
        if(cave.bot_lim_u > floor_level_max) then
            cave.bot_lim_u = cave.bot_lim_u - 1
        else
            floor_max_level = true
        end

        if(cave.top_lim_u < (cave.top_lim_l - 5)) then
            cave.top_lim_u = cave.top_lim_u + 1
            cave.min_offset = (3 - cave.top_lim_u)
        end
        if(cave.bot_lim_l > (cave.bot_lim_u + 5)) then
            cave.bot_lim_l = cave.bot_lim_l - 1
            cave.max_offset = (124 - cave.bot_lim_l)
        end

        change_offset = (roof_max_level and floor_max_level)

        if(change_offset) then
            if(offset_inc > 1) then 
                offset_inc = offset_inc - 1
            end
        end
    end

    if(change_offset) then
        offset_count = offset_count - 1
        if(offset_count == 0) then
            offset_count = offset_inc
            local offset = rnd_int(-3, 4)
            cave.offset = mid_int(cave.min_offset, cave.offset + offset, cave.max_offset)
        end
    end
end

--> Cave

function make_cave()
    cave = {}
    cave.col = 3
    cave.seg = {{["top"]=5, ["bot"]=119}}
    cave.top_lim_l = roof_level_min --how low can the ceiling go.
    cave.top_lim_u = 3 --ceiling cannot be higher than this value.
    cave.bot_lim_l = 124 --floor cannot be lower than this value.
    cave.bot_lim_u = floor_level_min --how high can the floor get.
    cave.offset = 0 -- The current offset of the above values.
    cave.min_offset = 0
    cave.max_offset = 0

    --insert more cave
    for i=1,128 do
        local seg = {}
        local up = rnd_int(-3, 4)
        local dwn = rnd_int(-3, 4)
        seg.top = mid_int(cave.top_lim_u, cave.seg[#cave.seg].top + up, cave.top_lim_l)
        seg.bot = mid_int(cave.bot_lim_u, cave.seg[#cave.seg].bot + dwn, cave.bot_lim_l)
        table.insert(cave.seg, seg)
    end
end

function update_cave()
    --remove the back of the cave
    for i=1,player.speed do
        table.remove(cave.seg, i)
        
        local seg = {}
        local up = rnd_int(-3, 4)
        local dwn = rnd_int(-3, 4)
        seg.top = mid_int(cave.top_lim_u + cave.offset, cave.seg[#cave.seg].top + up, cave.top_lim_l + cave.offset)
        seg.bot = mid_int(cave.bot_lim_u + cave.offset, cave.seg[#cave.seg].bot + dwn, cave.bot_lim_l + cave.offset)
        table.insert(cave.seg, seg)
    end
end

function draw_cave()
    for i=1,#cave.seg do
        local xpos = i-1
        draw_line(xpos, 0, xpos, cave.seg[i].top, cave.col)
        draw_line(xpos, 127, xpos, cave.seg[i].bot, cave.col)
    end
end

--> Bubbles
bubble_col = 10
bubble_num = 4
bubble_xthr = math.floor(128/bubble_num)

function new_bubble()
    b = {}
    b.r = 0
    b.x = 0
    b.y = 0
    b.vxt = 0
    b.vyt = 0
    b.vxc = 0
    b.vyc = 0
    b.spt = rnd_int(600) -- Spawn time.
    b.layer = 0

    return b
end

function spawn_bubble(b)
    b.r = rnd_int(1, 4)
    b.x = rnd_int(80, 128)
    b.y = 128 + b.r
    b.vxt = rnd_int(3, 9)
    b.vyt = rnd_int(3, 9)
    b.vxc = 0
    b.vyc = 0
    b.layer = rnd_int(0, 2)

    return b
end

function make_bubbles()
    bubbles={}
    for i=1,bubble_num do
        table.insert(bubbles,new_bubble())
    end
end

function update_bubbles()
    for i, b in ipairs(bubbles) do
        if(b.spt == 0) then
            b.vxc = b.vxc + 1
            b.vyc = b.vyc + 1
            if(b.vxc > b.vxt) then
                b.vxc = 0
                b.x = b.x - 1
            end
            if(b.vyc>b.vyt) then
                b.vyc = 0
                b.y = b.y - 1
            end
            if(((b.x + b.r) < 0) or ((b.y + b.r) < 0)) then
                b.spt = rnd_int(600)
            end
        else
            b.spt = b.spt - 1
            if(b.spt == 0) then
                spawn_bubble(b)
            end
        end
    end
end

function draw_bubbles(layer)
    for i, b in ipairs(bubbles) do
        if(b.layer == layer) then
            draw_circle(b.x, b.y, b.r, false, bubble_col)
        end
    end
end
