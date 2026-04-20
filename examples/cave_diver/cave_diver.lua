game_title = "Cave Diver"

--game variables
gravity = 0.1

function game_logic_init()
    player_died=true
    game_over=false
    start_pause = 60
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
    draw_bubbles()
    draw_cave()
    draw_player()

    score_string = "Your Score: "..player.score
    if(game_over) then
        draw_string(40, 44, "Game Over!", FONT_5X7_FIXED, 1, 0x0E)
        draw_string(30, 54, score_string, FONT_5X7_FIXED, 1, 0x0E)
        draw_string(20, 64, "Press A to restart.", FONT_5X7_FIXED, 1, 0x0E)
    else
        draw_string(2, 8, score_string, FONT_5X7_FIXED, 1, 0x0E)
    end
end


-->8

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
        player.dy = player.dy - 4
        phrase_play(0)
    end

    -- Move to new position
    player.y = player.y + player.dy

    -- Update score
    player.score = player.score + player.speed
end

function check_hit()
    for i=player.x,player.x+1 do
        if(not player.dead and cave[i+1].top > player.y) then
            player.dead=true
            player.dy=0
            phrase_play(2)
            if(player.y<cave[i+1].top) then
                player.y=cave[i+1].top
                break
            end
        elseif(cave[i+1].bot<player.y+7) then
            player.dead=true
            game_over=true
            phrase_play(1)
            if(player.y+7>cave[i+1].bot) then
                player.y=cave[i+1].bot-7
                break
            end
        end
    end
end

-->8
--cave variables
cave_col = 3

function make_cave()
    cave = {{["top"]=5, ["bot"]=119}}
    top = 40 --how low can the ceiling go.
    bot = 90 --how high can the floor get.

        --insert more cave
    for i=1,128 do
        local c = {}
        local up = math.floor(rnd_int(-3, 4))
        local dwn = math.floor(rnd_int(-3, 4))
        c.top=mid_int(3, cave[#cave].top + up, top)
        c.bot=mid_int(bot, cave[#cave].bot + dwn, 124)
        table.insert(cave, c)
    end
end

function update_cave()
    --remove the back of the cave
    if(#cave>player.speed) then
        for i=1,player.speed do
            table.remove(cave, i)
            
            local c = {}
            local up = math.floor(rnd_int(-3, 4))
            local dwn = math.floor(rnd_int(-3, 4))
            c.top=mid_int(3, cave[#cave].top + up, top)
            c.bot=mid_int(bot, cave[#cave].bot + dwn, 124)
            table.insert(cave, c)
        end
    end
end

function draw_cave()
    for i=1,#cave do
        local xpos=i-1
        draw_line(xpos,0,xpos,cave[i].top,cave_col)
        draw_line(xpos,127,xpos,cave[i].bot,cave_col)
    end
end

-->8
--bubbles
bubble_col = 10
bubble_num = 4
bubble_xthr = math.floor(128/bubble_num)

function new_bubble()
    b = {}
    b.r = rnd_int(1, 4)
    b.x = rnd_int(80, 128)
    b.y = 128 + b.r
    b.vxt = rnd_int(3, 7)
    b.vyt = rnd_int(3, 7)
    b.vxc = 0
    b.vyc = 0

    return b
end

function make_bubbles()
    bubbles={}
    table.insert(bubbles,new_bubble())
end

function update_bubbles()
	local b_cnt = #bubbles 
	
    if(b_cnt<bubble_num) then
        table.insert(bubbles, new_bubble())
    end

    for i, b in ipairs(bubbles) do
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
            table.remove(bubbles, i)
        end
    end
end

function draw_bubbles()
    for i, b in ipairs(bubbles) do
        draw_circle(b.x, b.y, b.r, false, bubble_col)
    end
end
