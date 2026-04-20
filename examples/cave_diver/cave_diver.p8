pico-8 cartridge // http://www.pico-8.com
version 43
__lua__
--game variables
gravity=0.2

function _init()
 player_died=true
 game_over=false
 make_bubbles()
 make_cave()
 make_player()
end

function _update()
 if(not game_over) then
  update_bubbles()
  update_cave()
  move_player()
  check_hit()
 else
  if(btnp(5)) _init() --restart
 end
end

function _draw()
 cls()
 draw_bubbles()
 draw_cave()
 draw_player()
 
 if(game_over) then
  print("game over!",44,44,7)
  print("your score:"..player.score,34,54,7)
  print("press ❎ to restart",24,64,7)
 else
  print("score:"..player.score,2,2,7)
 end
end


-->8

function make_player()
 player={}
 player.x=24    --position
 player.y=60
 player.dy=0    --fall speed
 player.sprite=1
 player.speed=2 --fly speed
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
 
 spr(player.sprite,player.x,player.y)
end

function move_player()
 player.dy+=gravity
 
 --jump
 if(not player.dead and btnp(2)) then
  player.dy-=5
  sfx(0)
 end
 
 --move to new position
 player.y+=player.dy
 
 --update score
 player.score+=player.speed
end

function check_hit()
 for i=player.x,player.x+1 do
  if(not player.dead and cave[i+1].top>player.y) then
   player.dead=true
   player.dy=0
   sfx(2)
   if(player.y<cave[i+1].top) then
   	player.y=cave[i+1].top
    break
   end
  elseif(cave[i+1].bot<player.y+7) then
   player.dead=true
   game_over=true
   sfx(1)
   if(player.y+7>cave[i+1].bot) then
   	player.y=cave[i+1].bot-7
   	break
   end
  end
 end
end
-->8
--cave variables
cave_col=8

function make_cave()
 cave={{["top"]=5,["bot"]=119}}
 top=45 --how low can the ceiling go.
 bot=85 --how hight can the floor get.
end

function update_cave()
 --remove the back of the cave
 if(#cave>player.speed) then
  for i=1,player.speed do
   del(cave,cave[1])
  end
 end
 
 --add more cave
 while(#cave<128) do
  local c={}
  local up=flr(rnd(7)-3)
  local dwn=flr(rnd(7)-3)
  c.top=mid(3,cave[#cave].top+up,top)
  c.bot=mid(bot,cave[#cave].bot+dwn,124)
  add(cave,c)
 end
end

function draw_cave()
 for i=1,#cave do
  local xpos=i-1
  line(xpos,0,xpos,cave[i].top,cave_col)
  line(xpos,127,xpos,cave[i].bot,cave_col)
 end
end
-->8
--bubbles
bubble_col=6
bubble_num=6
bubble_xthr=(128/bubble_num)

function new_bubble()
 b={}
 b.r=rnd(3)+1
 b.x=rnd(48)+80
 b.y=128+b.r
 b.vxt=rnd(3)
 b.vyt=rnd(3)
 b.vxc=0
 b.vyc=0
 
 return b
end

function make_bubbles()
 bubbles={}
 add(bubbles,new_bubble())
end

function update_bubbles()
	local b_cnt=#bubbles 
	local b_xthr=128
	b_xthr-=rnd(bubble_xthr)+(bubble_xthr/2)
	
 if(b_cnt<bubble_num) then
  add(bubbles,new_bubble())
 end

 for b in all(bubbles) do
  b.vxc+=1
  b.vyc+=1
  if(b.vxc>b.vxt) then
   b.vxc=0
   b.x-=1
  end
  if(b.vyc>b.vyt) then
   b.vyc=0
   b.y-=1
  end
  if(b.x+b.r<0 or b.y+b.r<0) then
   del(bubbles,b)
  end
 end
end

function draw_bubbles()
 for b in all(bubbles) do
  circ(b.x,b.y,b.r,bubble_col)
 end
end
 


__gfx__
0000000000ffff0000ffff00ef0fe0fe000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
000000000ffffff00ffffff0ef0fe0fe000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
007007000ff3f3f00ff3f3f0eefeefee000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
000770000ff3f3f00ff3f3f0eeeeeeee000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
000770000ffffff0ffffffff0eeeeee0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
007007000ffffff0ffeffeff0e33e330000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
000000000ffefef0fe0ef0ef0eeeeee0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
000000000ffefef0fe0ef0ef00eeee00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
__sfx__
010802000c360133603d3003230000300003000030000300003000030000300003000030000300003000030000300003000030000300003000030000300003000030000300003000030000300003000030000300
010a10000c3500c3500c3500c35005350053500535005350023500235002350023500235002350023500235006300063000030000300003000030000300003000030000300003000030000300003000030000300
010202002e6500e650000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
