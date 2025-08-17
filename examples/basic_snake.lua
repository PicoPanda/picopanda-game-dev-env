-- Snake Game for PicoPanda - Basic Test Version
-- Global variables
local snake = {}  -- Table to store all snake segments
local direction_x = 1  -- Start moving right
local direction_y = 0
local move_counter = 0  -- Counter to control movement speed
local move_delay = 20   -- Move every 20 frames (adjust this to control speed)
local food_x, food_y     -- Food position
local score = 0          -- Current score
local game_over = false  -- Game over state
local grid_size = 4  -- 4x4 pixel grid
local screen_width = 128
local screen_height = 128
local grid_width = screen_width / grid_size
local grid_height = screen_height / grid_size

function game_logic_init()
    -- Initialize snake (start in middle, 3 segments long)
    snake = {}
    for i = 1, 3 do
        table.insert(snake, {x = grid_width/2 - i + 1, y = grid_height/2})
    end
    
    -- Reset direction and speed
    direction_x = 1
    direction_y = 0
    move_counter = 0
    move_delay = 20  -- Start at normal speed
    score = 0
    game_over = false
    
    -- Spawn initial food
    spawn_food()
    
    print("Snake game initialized!")
    print("Snake head at: " .. snake[1].x .. "," .. snake[1].y)
end

function game_logic_loop()
    -- Handle input (always check for input)
    local buttons = get_button_status()
    
    if game_over then
        -- Check for restart
        if buttons.up_pressed or buttons.down_pressed or 
           buttons.left_pressed or buttons.right_pressed then
            game_logic_init()
        end
        -- Always draw the game over screen when game is over
        draw_game()
        return
    end
    
    if buttons.up_pressed and direction_y == 0 then
        direction_x = 0
        direction_y = -1
    elseif buttons.down_pressed and direction_y == 0 then
        direction_x = 0
        direction_y = 1
    elseif buttons.left_pressed and direction_x == 0 then
        direction_x = -1
        direction_y = 0
    elseif buttons.right_pressed and direction_x == 0 then
        direction_x = 1
        direction_y = 0
    end
    
    -- Move snake only every few frames (controlled speed)
    move_counter = move_counter + 1
    if move_counter >= move_delay then
        move_snake()
        move_counter = 0
    end
    
    -- Always draw (smooth visual updates)
    draw_game()
end

function move_snake()
    -- Get head position
    local head = snake[1]
    local new_head = {x = head.x + direction_x, y = head.y + direction_y}
    
    -- Simple wall wrapping
    if new_head.x < 0 then new_head.x = grid_width - 1 end
    if new_head.x >= grid_width then new_head.x = 0 end
    if new_head.y < 0 then new_head.y = grid_height - 1 end
    if new_head.y >= grid_height then new_head.y = 0 end
    
    -- Check self collision
    if check_self_collision(new_head) then
        game_over = true
        return
    end
    
    -- Check if snake ate food
    if new_head.x == food_x and new_head.y == food_y then
        score = score + 10
        
        -- Increase speed very gradually (decrease delay)
        if move_delay > 2 then  -- Don't go faster than 10 frames
            move_delay = move_delay - 0.5  -- Very gradual speed increase
        end
        
        -- Add new head (snake grows)
        table.insert(snake, 1, new_head)
        
        -- Spawn new food
        spawn_food()
    else
        -- Move snake (remove tail, add new head)
        table.remove(snake)
        table.insert(snake, 1, new_head)
    end
end

function check_self_collision(new_head)
    -- Check new head position against all body segments
    for i = 2, #snake do
        if new_head.x == snake[i].x and new_head.y == snake[i].y then
            return true
        end
    end
    return false
end

function spawn_food()
    local attempts = 0
    local valid_position = false
    
    -- Keep trying until we find a valid position
    while not valid_position and attempts < 100 do
        food_x = math.random(0, grid_width - 1)
        food_y = math.random(0, grid_height - 1)
        
        valid_position = true
        
        -- Check if food spawns on any snake segment
        for i = 1, #snake do
            if food_x == snake[i].x and food_y == snake[i].y then
                valid_position = false
                break
            end
        end
        
        attempts = attempts + 1
    end
end

function draw_game()
    -- Clear screen (draw black background)
    draw_rectangle(0, 0, screen_width, screen_height, true, 0x00)
    
    -- Draw snake segments
    for i = 1, #snake do
        local segment = snake[i]
        local x = segment.x * grid_size
        local y = segment.y * grid_size
        
        -- Head (different color)
        if i == 1 then
            draw_rectangle(x, y, grid_size, grid_size, true, 0x04)
        else
            -- Body segments
            draw_rectangle(x, y, grid_size, grid_size, true, 0x04)
        end
    end
    
    -- Draw food
    local food_screen_x = food_x * grid_size
    local food_screen_y = food_y * grid_size
    draw_rectangle(food_screen_x, food_screen_y, grid_size, grid_size, true, 0x0F)
    
    -- Draw score and debug info (positioned properly for 4-bit screen)
    draw_string(0, 120, "Score: " .. score, FONT_4X5_FIXED, 1, 0x0F)
    
    -- Draw game over screen if needed
    if game_over then
        draw_game_over()
    end
end

function draw_game_over()
    -- Draw semi-transparent overlay
    draw_rectangle(20, 40, 88, 48, true, 0x08)
    draw_rectangle(22, 42, 84, 44, true, 0x00)
    
    -- Draw game over text
    draw_string(41, 50, "GAME OVER", FONT_4X5_FIXED, 1, 0x0F)
    draw_string(30, 60, "Final Score: " .. score, FONT_4X5_FIXED, 1, 0x0F)
    draw_string(35, 70, "Press any key", FONT_4X5_FIXED, 1, 0x0F)
end