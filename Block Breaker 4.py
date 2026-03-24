import pyxel

# Ball class
# Manages settings and movement of the ball within the screen
class Ball:
     # Coefficient that determines the ball's movement speed
     speed=2.0
     
     def __init__(self):
         # Initialization process when a Ball object is created
         # By consolidating in restart(), reusability is improved
         self.restart()
         
     # Setting the ball's initial state
     def restart(self):
         # Initial position
         self.x = 100
         self.y = 150

         # Launch angle
         # Launches at a random angle between 30~150 degrees
         # Used at the start of the game or when the ball is generated
         # When adding a ball, use launch()
         angle = pyxel.rndi(30, 150)
         self.vx = pyxel.cos(angle)
         self.vy = pyxel.sin(angle)

         # Manages values used for inserting images
         # Position to cut from the image bank
         self.u=32
         self.v=0
         # Image size (8×8)
         self.w=8
         self.h=8

         # Flag indicating whether the ball has been launched
         # Initially not launched
         self.launched = False

     # Settings for launching the ball
     # Used when pressing the space key to launch the ball
     def launch(self):
         # Launches at a random angle between 30~150 degrees
         angle = pyxel.rndi(30, 150)
         self.vx = pyxel.cos(angle)
         self.vy = pyxel.sin(angle)

         # Enable launched flag
         self.launched = True    

     # Defines ball movement
     def move(self):
         # Do not move if not launched
         if not self.launched:
            return

         # Save the previous frame's position
         # Used to determine collision direction
         # Reference: Chat GPT
         self.prev_x = self.x
         self.prev_y = self.y
         
         # Divide movement according to ball speed
         # When speed is high, the movement in one frame is calculated multiple times
         # To prevent passing through blocks (reference: Chat GPT)
         step = int(Ball.speed)
         if step < 1:
            step = 1
         # Divide movement amount by speed value
         dx = self.vx * Ball.speed / step
         dy = self.vy * Ball.speed / step

         # Add divided movement to ball's motion
         for _ in range(step):
            self.x += dx
            self.y += dy
         
         # Reverse movement direction if hitting left or right wall
         if self.x<0 or self.x + self.w >= 200:
             self.vx = -self.vx
             
         # Reverse movement direction if hitting top wall
         if self.y < 0:
            self.vy = -self.vy

     # Processing when the ball hits the pad
     def bounce_pad(self, pad):
          
         # Prevent the ball from sinking into the pad
         self.y = pad.y - self.h

         # Save x-direction of the ball
         if self.vx >= 0:
              dir_x = 1
         else:     
              dir_x = -1

              
         # Press W key to decrease reflection angle (shallow horizontal bounce)
         if pyxel.btn(pyxel.KEY_W):
              angle = 35
              
         # Press S key to increase reflection angle (steep upward bounce)
         elif pyxel.btn(pyxel.KEY_S):
              angle = 80
              
         # If nothing is pressed, just reflect normally
         else:
              self.vy *= -1
              return
          
         # Calculate velocity vector for specified angle
         self.vx = dir_x * pyxel.cos(angle)
         self.vy = -pyxel.sin(angle)
          
     def draw(self):
         # Draw the ball on the screen
         pyxel.blt(self.x, self.y, 0, self.u, self.v, self.w, self.h)
         
# Pad class
# Manages settings and movement of the pad
class Pad:
    def __init__(self):
         # Standard pad settings
         # Coordinates to display the pad on the screen
         self.x=100
         self.y=150
         # Pad size
         self.w=32
         self.h=8
         # Save normal size (used when enlarging/reverting the pad)
         self.base_w = 32
         # Flag for enlarged state; inactive if no special effect
         self.large = False 

    # Checks if the pad collides with a ball
    # ball is taken as an argument to handle cases where multiple balls exist due to special effects
    def catch(self,ball):
         
         # Collision detection between ball and pad
         # This method only checks for collision; actual bounce processing
         # is handled in App class after detection
         # Ball.bounce_pad() is called there
         return (ball.y + ball.h >= self.y and ball.x + ball.w >= self.x
                 and ball.x <= self.x + self.w)

    # Draw the pad on the screen    
    def draw(self):
        # When special effect is active, pad becomes larger; adjust drawing accordingly
        # Effect applied
        if self.large:
            pyxel.blt(self.x, self.y, 0, 40, 0, 48, 8)
        # Normal
        else:
            pyxel.blt(self.x, self.y, 0, 0, 0, 32, 8)
            
    
# Block class
# Manages block position, type, durability, destruction status, etc.
class Block:
    def __init__(self,x,y,type='normal'):
        # Initial position
        self.x=x
        self.y=y

        # Size of one block
        self.w=16
        self.h=8
        
        # Block type
        # Used for determining effects, images, and durability for various block types
        self.type=type
        
        # Flag for whether block is destroyed
        self.alive=True

        # Block durability
        # Point blocks have durability of 2
        if type=='point':
           self.hp=2
        # Other blocks have durability of 1
        else:
           self.hp=1 
        
        # Image position for each block type
        if type=='normal':
            self.u=16
            self.v=26

        elif type=='large':
            self.u=16
            self.v=10
            
        elif type=='slow':
            self.u=0
            self.v=18

        elif type=='ball':
            self.u=0
            self.v=26

        elif type=='point':
            self.u=0
            self.v=10

        elif type=='death':
            self.u=16
            self.v=18
            
    # Draw block
    def draw(self):
         
        # Only draw blocks that are not destroyed
        if self.alive:
            pyxel.blt(self.x, self.y, 0, self.u, self.v, self.w, self.h)

        
# Define block positions for each stage
# Block(x-coordinate, y-coordinate, type). Type omitted defaults to normal block
# By defining here, stage selection and drawing by stage become easier

# Easy stage block positions
def stage_easy():
      
    return [Block(22, 25),Block(39, 25, "slow"),Block(56, 25),
            Block(73, 25),Block(90, 25, "large"),Block(107, 25),
            Block(124, 25),Block(141, 25, "ball"),Block(158, 25),
            Block(39, 34),Block(73, 34),Block(107, 34),
            Block(141, 34),Block(22, 43),Block(56, 43, "point"),
            Block(90, 43),Block(124, 43, "point"),Block(158, 43),
            Block(22, 52),Block(39, 52),Block(56, 52),
            Block(73, 52),Block(90, 52),Block(107, 52),
            Block(124, 52),Block(141, 52),Block(158, 52)]

# Normal stage block positions
def stage_normal():
    return [Block(22, 25, "death"),Block(39, 25, "point"),Block(56, 25),
            Block(73, 25),Block(90, 25),Block(107, 25),
            Block(124, 25),Block(141, 25),Block(158, 25),
            Block(22,34,"point"),Block(39, 34, "point"),Block(73, 34),
            Block(107, 34),Block(141, 34),Block(22, 43),
            Block(158, 34),Block(56, 43, "slow"),Block(90, 43),
            Block(124, 43, "ball"),Block(158, 43),Block(39, 52, "ball"),
            Block(73, 52),Block(107, 52),Block(141, 52, "large"),
            Block(22, 60),Block(39, 60),Block(56, 60),
            Block(73, 60),Block(90, 60),Block(107, 60),
            Block(124, 60),Block(141, 60),Block(158, 60)]

# Hard stage block positions
def stage_hard():
    return [Block(15, 20),Block(32, 20, "slow"),Block(49, 20),
            Block(66, 20),Block(83, 20),Block(100, 20) ,
            Block(117, 20),Block(134, 20),Block(151, 20, "ball"),
            Block(168, 20),Block(22, 29),Block(39, 29),
            Block(56, 29, "large"),Block(73, 29),Block(90, 29, "point"),
            Block(107, 29),Block(124, 29, "slow"),Block(141, 29),
            Block(158, 29),Block(39, 38),Block(73, 38, "point"),
            Block(90, 38, "death"),Block(107, 38, "point"),Block(141, 38),
            Block(22, 47),Block(39, 47, "ball"),Block(56, 47),
            Block(73, 47),Block(90, 47, "point"),Block(107, 47),
            Block(124, 47),Block(141, 47, "large"),Block(158, 47),
            Block(15, 56),Block(32, 56),Block(49, 56),
            Block(66, 56),Block(83, 56),Block(100, 56) ,
            Block(117, 56),Block(134, 56),Block(151, 56),
            Block(168, 56)]

# App class
# Manages the overall game
class App:
    def __init__(self):
        # Screen size (width 200, height 170) 
        pyxel.init(200,170)
        
        # Load image resources
        pyxel.load('my_resource.pyxres')

        # Load sound effects (used when breaking blocks, etc.)
        pyxel.sound(0).set(notes='A2C3', tones='TT', volumes='33', effects='NN', speed=10)
        pyxel.sound(1).set(notes='C3A2', tones='TT', volumes='33', effects='NN', speed=10)

        # Variable for scene management (used to set behavior for each screen state)
        # Types are:
        # "title"  : Title screen
        # "select" : Stage selection screen
        # "play"   : During gameplay
        # "result" : After game ends
        self.scene = "title"

        # Selected stage (easy/normal/hard)
        self.stage = None   

        # Manage balls in a list (to handle multiple balls from special effects)
        self.balls=[Ball()]

        # Pad
        self.pad=Pad()

        # List to store blocks
        # Blocks corresponding to the selected stage will be stored here
        self.blocks=[]

        # Player score, initially 0
        self.score=0

        # Flags to manage game state
        # Game over
        self.game_over = False
        # Game clear
        self.clear = False

        # End frame for item effects
        # Used with frame_count to manage effect duration
        
        # Slow ball speed
        self.slow_time=0
        # Extra ball
        self.ball_time=0
        # Pad enlargement
        self.large_time=0
        # 100x point
        self.point_time = 0

        # Call update (logic) and draw (render) every frame
        pyxel.run(self.update,self.draw)

    # Reset the game to initial state
    # Called after stage selection or restart
    def reset(self):

        # Reset pad and ball to initial state
        self.balls=[Ball()]
        self.pad=Pad()

        # Generate blocks according to selected stage
        # easy
        if self.stage == "easy":
           self.blocks = stage_easy()
        # normal
        elif self.stage == "normal":
           self.blocks = stage_normal()
        # hard   
        elif self.stage == "hard":
           self.blocks = stage_hard()
           
        # Reset score
        self.score=0

        # Reset state flags
        self.game_over = False
        self.clear = False

        # Remove all item effects
        self.slow_time=0
        self.ball_time=0
        self.large_time=0
        self.point_time = 0

        # Restore ball speed
        Ball.speed = 2.0
        
    # Method to handle effects triggered when blocks are destroyed
    # Apply different effects based on block type
    def effect(self,block):
         
        # point block: 100x points for 10 seconds
        if block.type == "point":
            # Use frame_count + 300 frames (10 sec) as effect start time
            # Used later to determine effect end
            self.point_time = pyxel.frame_count + 300

        # Normal score  
        add=10 
        # If point block effect is active, all block scores are 100x
        if pyxel.frame_count < self.point_time:
            add*=100    

        # large block: enlarge pad for 10 seconds
        if block.type == "large":
            # Enable pad enlargement flag; pad moves differently when enlarged
            self.pad.large = True
            # Change pad width (image cutout area changes)
            self.pad.w = 48
            # Use frame_count + 300 frames (10 sec) for effect duration
            self.large_time = pyxel.frame_count+300

        # slow block: ball speed decreases for 10 seconds
        if block.type == "slow":
            # Speed becomes 1.0
            Ball.speed=1.0
            # Use frame_count + 300 frames (10 sec) for effect duration
            self.slow_time = pyxel.frame_count+300

        # ball block: add extra ball for 10 seconds
        if block.type == "ball":
            # Place new ball on top of pad
            ball_2 = Ball()
            ball_2.x = self.pad.x + self.pad.w // 2
            ball_2.y = self.pad.y - ball_2.h
            # Launch immediately
            ball_2.launch()
            # Add to ball list
            self.balls.append(ball_2)
            # Use frame_count + 300 frames (10 sec) for effect duration
            self.ball_time = pyxel.frame_count+300

        # death block: destroy results in immediate game over
        if block.type == "death":
            # Play sound effect when destroyed
            pyxel.play(0, 1)
            # Game over immediately
            self.game_over = True
            return

        # Add score
        self.score += add

    # Called every frame for game logic
    def update(self):

        # Initially display title screen
        if self.scene=="title":

            # Press space to go to stage selection
            if pyxel.btnp(pyxel.KEY_SPACE):
                 self.scene = "select"
            return

        # Stage selection screen
        if self.scene == "select":

           # Keys 1~3 for difficulty selection
           # Key 1: easy stage
           if pyxel.btnp(pyxel.KEY_1):
              self.stage = "easy"
              self.reset()
              self.scene="play"
              
           # Key 2: normal stage
           elif pyxel.btnp(pyxel.KEY_2):
              self.stage = "normal"
              self.reset()
              self.scene="play"
              
           # Key 3: hard stage
           elif pyxel.btnp(pyxel.KEY_3):
              self.stage = "hard"
              self.reset()
              self.scene="play"
              
           return
     
        # Post-play selection screen
        if self.scene == "result":
             
           # R key: retry (same stage)
           if pyxel.btnp(pyxel.KEY_R):
              self.reset()
              self.scene = "play"

           # T key: return to title
           if pyxel.btnp(pyxel.KEY_T):
              self.scene = "title"
              self.stage = None
           return

        # If game over or cleared, show result screen
        if self.game_over or self.clear:
           self.scene="result"
           return

        # Press space to launch ball
        if pyxel.btnp(pyxel.KEY_SPACE):
            for ball in self.balls:
                if not ball.launched:
                    ball.launch()
            
        # Apply same logic to each ball
        for ball in self.balls:

            # If not launched, fix ball on top of pad
            if not ball.launched:
                ball.x = self.pad.x + self.pad.w // 2 - ball.w // 2
                ball.y = self.pad.y - ball.h
            # Move if launched
            else:
                ball.move()

            # Bounce if hitting pad
            if self.pad.catch(ball) and ball.vy > 0:
                ball.bounce_pad(self.pad)

            # Game over if ball falls
            if ball.y > 170:
                pyxel.play(0, 1)
                # Enable game over flag and go to result screen
                self.game_over=True

        # Pad follows mouse x-coordinate
        self.pad.x = pyxel.mouse_x
        
        # Check if item effects end
        # If current frame exceeds effect start time + 10 sec (set in effect()), effect ends
        # Check pad enlargement effect
        if pyxel.frame_count > self.large_time:
                # Disable enlargement
                self.pad.large = False
                # Reset pad width
                self.pad.w = self.pad.base_w

        # Check extra ball effect
        if pyxel.frame_count > self.ball_time:
                # Remove additional balls when effect ends
                self.balls = [self.balls[0]]

        # Check slow ball effect
        if pyxel.frame_count > self.slow_time:
                # Restore original speed
                Ball.speed = 2.0     

        # Collision detection between blocks and balls
        # Make block variable usable
        for block in self.blocks:
             # Apply only to undestroyed blocks
             if block.alive:
                  # Make ball variable usable
                  for ball in self.balls:
                       if (ball.x < block.x + block.w and ball.x + ball.w > block.x
                           and ball.y < block.y + block.h and ball.y + ball.h > block.y):

                           # Play sound when block is destroyed
                           pyxel.play(0, 0)

                           # Determine top/bottom or left/right collision and bounce ball accordingly (ref: Chat GPT)
                           # If top/bottom collision, reverse y-direction
                           if (ball.prev_y + ball.h <= block.y or ball.prev_y >= block.y + block.h):
                                ball.vy *= -1
                           # If left/right collision, reverse x-direction     
                           else:
                                ball.vx *= -1

                           # Reduce block durability when ball hits
                           block.hp-=1

                           # Destroy block if hp<=0 and apply effect for special blocks
                           if block.hp<=0:
                              block.alive=False      
                              self.effect(block)

        # Clear check                      
        clear_flag = True
        # Make block variable usable
        for block in self.blocks:
            # Ignore death blocks; if any other block is alive, not cleared
            if block.type != "death" and block.alive:
                clear_flag = False
        # If cleared, enable clear flag and show result screen
        if clear_flag:
            self.clear = True          
        
    # Called every frame for rendering
    def draw(self):
        # Clear screen with black
        pyxel.cls(0)

        # Title screen
        if self.scene=="title":
            # Display title text as images
            pyxel.blt(26,68,0,0,40,60,16)
            pyxel.blt(92,68,0,0, 56, 84,16)
            # Display "PRESS SPACE TO START" in white
            pyxel.text(60, 110, "PRESS SPACE TO START", 7)
            return

        # Stage selection screen
        if self.scene == "select":
           # Display "SELECT STAGE" in yellow; other stage info in white
           pyxel.text(60, 55, "SELECT STAGE", 10)
           pyxel.text(60, 85, "1 : EASY", 7)
           pyxel.text(60,105, "2 : NORMAL", 7)
           pyxel.text(60,125, "3 : HARD", 7)
           return

        # Post-game selection screen
        if self.scene == "result":
           # Display "CLEAR!" in blue if cleared
           if self.clear:
              pyxel.text(80, 60, "CLEAR!", 11)
           # Display "GAME OVER" in red if game over
           else:
              pyxel.text( 80, 60, "GAME OVER", 8)

           # Display other instructions and score in white
           pyxel.text(80,100, "R : RETRY", 7)
           pyxel.text(80,110, "T : TITLE", 7)
           pyxel.text(80, 80, "SCORE:" + str(self.score),7)
           return

        # Gameplay screen
        # Draw balls
        for ball in self.balls:
            ball.draw()

        # Draw pad
        self.pad.draw()
        
        # Draw blocks
        for block in self.blocks:
            block.draw()
        # Draw score
        pyxel.text(5, 5, "SCORE:" + str(self.score), 7)    
        
App()    
