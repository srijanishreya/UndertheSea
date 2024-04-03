"""
    Srijani Shreya
    Code ToolKit: Python - Spring 2024
    Midterm Project - Under the Sea
    March 26, 2023
"""

obstacles = []
num_obstacles = 11  # Total number of obstacles
game_over = False
you_win = False
game_over_frame = -1
reset_delay = 2000  # Time in milliseconds to wait before resetting the game
level_duration = 2000  # Time in milliseconds to display the level message
level_frame = -1
level = 1
max_levels = 5  # Total number of levels
obstacle_speeds = [0.75, 1, 1.25, 1.5, 1.75]  # Different speeds for each level
last_obstacle_time = 0  # Variable to track the time when the last obstacle was added
screen_width = 600  # Set the screen width
screen_height = 800  # Set the screen height
goal_x = screen_width / 2 - 25  # Set the x-coordinate for the goal (adjusted for image size)
goal_y = screen_height - 100  # Set the y-coordinate for the goal (adjusted for image size)
instructions_displayed = False  # Flag to track if instructions have been displayed
background_image = None  # Global variable to store the background image
fish_image = None  # Global variable to store the fish image
treasure_image = None  # Global variable to store the treasure chest image
diver_image = None  # Global variable to store the diver image
bubbles = []  # List to store bubble positions and velocities
bubble_image = None  # Global variable to store the bubble image

def setup():
    size(screen_width, screen_height)
    global bubble_image, last_bubble_time, background_image, fish_image, treasure_image, diver_image, player_x, player_y, game_over, you_win, game_over_frame, level_frame, level, last_obstacle_time, instructions_displayed
    background_image = loadImage("underthesea.jpg")  # background image here
    fish_image = loadImage("shark.png")  #shark image here
    treasure_image = loadImage("TreasureChest.png")  # treasure chest image here
    diver_image = loadImage("diver.png")  # diver image here
    fish_image.resize(100, 0)  # Resize the shark image width to 100 pixels, maintain aspect ratio
    treasure_image.resize(50, 0)  # Resize the treasure chest image width to 50 pixels, maintain aspect ratio
    diver_image.resize(50, 0)  # Resize the diver image width to 50 pixels, maintain aspect ratio
    bubble_image = loadImage("bubble.png")  # bubble image 
    bubble_image.resize(70, 0)
    
    player_x = width / 2
    player_y = 50  # Starting position of the player at the top
    game_over = False
    you_win = False
    game_over_frame = -1
    level_frame = -1
    level = 1
    last_obstacle_time = 0
    instructions_displayed = False
    reset_level()
    last_bubble_time = millis()
    
    update_bubbles()

def reset_level():
    global obstacle_speeds, obstacles
    obstacles = []
    for i in range(num_obstacles):
        y_pos = random(150, screen_height - 150)  # Randomize y position excluding player and goal rows
        obstacles.append({
            'x': width / (num_obstacles + 1) * (i + 1),  # Evenly spaced obstacles
            'y': y_pos,
            'speed': obstacle_speeds[level - 1],  # Set obstacle speed based on current level
            'direction': 1
        })

    
def draw():
    global bubbles, background_image, fish_image, treasure_image, diver_image, player_x, player_y, game_over, you_win, game_over_frame, level_frame, level, last_obstacle_time, instructions_displayed
    if not instructions_displayed:
        display_instructions()
    else:
        # Draw background image first
        image(background_image, 0, 0, width, height)
       
        # Draw diver (you, the player)
        image(diver_image, player_x, player_y, 60, 60)  # Display diver image
        
        # Draw sharks (the obstacles)
        for obstacle in obstacles:
            image(fish_image, obstacle['x'], obstacle['y'], 80, 80) 
            obstacle['x'] += obstacle['speed'] * obstacle['direction']
            if obstacle['x'] < -15 or obstacle['x'] > 550:
                obstacle['direction'] *= -1
                
        # Draw treasure chest (goal)
        image(treasure_image, goal_x, goal_y, 80, 80)  # Display treasure chest image
        
        # Checking for collision with sharks (obstacles)
        for obstacle in obstacles:
            obstacle_center_x = obstacle['x'] + 40  # Adjust for center of obstacle image
            obstacle_center_y = obstacle['y'] + 40  # Adjust for center of obstacle image
            if dist(player_x + 30, player_y + 30, obstacle['x']+50, obstacle['y']+50) < 35:
                game_over = True
                game_over_frame = millis()
        
        # Checking for collision with goal (treasure chest)
        if dist(player_x + 30, player_y + 30, goal_x + 40, goal_y + 40) < 35:
            if level == max_levels:
                you_win = True
            else:
                next_level()

        if you_win:
            fill(255, 255, 0)
            textSize(50)
            text("You Win!", 200, height/2)
            update_bubbles()
            return
        
        if game_over:
            if millis() - game_over_frame >= reset_delay:
                reset_game()  # Reset the game after delay
                return
            else:
                fill(255, 255, 0)
                textSize(50)
                text("Game Over", 200, height/2)
                update_bubbles()
                return
        
        # Display level message
        if level_frame != -1 and millis() - level_frame <= level_duration:
            fill(255, 255, 0)
            textSize(50)
            text("Level " + str(level), 250, height/2)
            update_bubbles()
            return
       
        update_bubbles() 

def update_bubbles():
    global bubbles, last_bubble_time
    if millis() - last_bubble_time > 600:  # new bubble will pop out every 600 milliseconds
        bubbles.append({'x': random(width), 'y': height, 'speed': 0.75})
        last_bubble_time = millis()

    # Display and update existing bubbles
    for bubble in bubbles:
        image(bubble_image, bubble['x'], bubble['y'], 40, 40)  # Display bubble image
        bubble['y'] -= bubble['speed']  # Move the bubble up based on its speed
        if bubble['y'] < -30:  # Reset bubble position if it goes off-screen
            bubbles.remove(bubble)

def reset_player():
    global player_x, player_y
    player_x = width / 2
    player_y = 50  # Reset player position to the top
  
def next_level():
    global level, level_frame, obstacle_speeds, you_win
    if level < max_levels:  # Checks if the current level is not the maximum level
        level += 1
        if level == 2:
            obstacle_speeds[1] += 0.5  # Increase obstacle speed for level 2
        elif level == 3:
            obstacle_speeds[2] += 0.5  # Increase obstacle speed for level 3
        elif level == 4:
            obstacle_speeds[3] += 0.5  # Increase obstacle speed for level 4
        elif level == 5:
            obstacle_speeds[4] += 0.5  # Increase obstacle speed for level 5
        reset_level()  # Reset obstacles for the next level
        reset_player()  # Reset player position for the next level
        level_frame = millis()  # Start the next level

    else:
        you_win = True  # Set you_win flag to True when reaching level 5
        update_bubbles()
        level = 1  # Reset level to 1 after winning all levels
        reset_level()  # Reset obstacles for level 1
        reset_player()  # Reset player position for level 1
        level_frame = millis()  # Start level 1
        
    update_bubbles()

def reset_game():
    global level_frame, last_obstacle_time, instructions_displayed, level, game_over, you_win
    level = 1  # Reset level to 1 when resetting the game
    game_over = False
    you_win = False
    reset_level()  # Reset obstacles for level 1
    reset_player()  # Reset player position for level 1
    level_frame = millis()  # Start the game
    
    update_bubbles()

def display_instructions():
    global instructions_displayed, level_frame, background_image
    image(background_image, 0, 0, width, height)
    if millis() <= 10000:  # Display instructions for the first 10 seconds
        
        # Add blue rectangle
        noStroke()
        fill(0, 128, 128, 200) # teal color
        rect(30, 170, 550, 290)  # Rectangle position and size
        
        # Add text on top of the blue rectangle
        textFont(createFont("Arial Bold", 50)) 
        fill(255)  # White color for text
        textSize(12.5)
        text("As a skilled scuba diver, you're tasked with retrieving a pirate's treasure chest", 40, 200)
        text("discovered in a recent underwater excavation. Your mission is perilous; navigating", 40, 230)
        text("through treacherous waters infested with menacing sharks. Armed with only your ", 40, 260)
        text("wits and equipment, you plunge into the depths, evading the razor-sharp teeth of", 40, 290)
        text("these predators. The murky depths conceal hidden dangers and obstacles, testing", 40, 320)
        text("your courage and agility. With each cautious move, you inch closer to the fabled", 40, 350)
        text("treasure, knowing that one wrong step could spell disaster. Will you outsmart the", 40, 380)
        text("sharks and claim the pirate's riches, or become another victim of the unforgiving sea?", 40, 410)
        text("Use arrow keys to move.", 40, 440)
        
        # Add title "Under the Sea"
        textFont(createFont("Impact", 50)) 
        fill(40, 220, 250, 200)  # White color for text
        textSize(50)
        text("Under the Sea", 150, 100)  # the title at the top center of the screen
        
    else:
        instructions_displayed = True  # Set instructions flag to True after 10 seconds
        level_frame = millis()  # Start the game after 10 seconds
        
    update_bubbles()

def keyPressed():
    global player_x, player_y
    if keyCode == LEFT and player_x > 0:
        player_x -= 10
    elif keyCode == RIGHT and player_x < width - 20:
        player_x += 10
    elif keyCode == UP and player_y > 0:
        player_y -=10
    elif keyCode == DOWN and player_y < height - 20:
        player_y += 10
