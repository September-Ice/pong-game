#!/usr/bin/env python
import sys
sys.path.insert(1, sys.argv[1])
from duels import Subscriber
print('(Python) I am coming oooo!!!!!')
game = Subscriber(1000)
print('(Python) Game is:',dir(game))
init_msg = game.get_init()
print("(Python) Data Init is:",dir(init_msg) )

print('(Python) init msg p1 is:',init_msg.p1.x)
print('(Python) init msg p2 is:',init_msg.p2.y)

def flip(y):
    return 335 - y

# Import the pygame library and initialise the game engine
import pygame
#from paddle import Paddle
BLACK = (0,0,0)

class Paddle(pygame.sprite.Sprite):
    #This class represents a paddle. It derives from the "Sprite" class in Pygame.
    
    def __init__(self, color, width, height):
        # Call the parent class (Sprite) constructor
        super().__init__()
        
        # Pass in the color of the paddle, and its x and y position, width and height.
        # Set the background color and set it to be transparent
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
 
        # Draw the paddle (a rectangle!)
        pygame.draw.rect(self.image, color, [0, 0, width, height])
        
        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()
        
    def moveUp(self, pixels):
        self.rect.y -= pixels
		#Check that you are not going too far (off the screen)
        if self.rect.y < 0:
          self.rect.y = 0
          
    def moveDown(self, pixels):
        self.rect.y += pixels
	#Check that you are not going too far (off the screen)
        if self.rect.y > 400:
          self.rect.y = 400

#from ball import Ball
from random import randint
BLACK = (0, 0, 0)

class Ball(pygame.sprite.Sprite):
    #This class represents a car. It derives from the "Sprite" class in Pygame.
    
    def __init__(self, color, width, height):
        # Call the parent class (Sprite) constructor
        super().__init__()
        
        # Pass in the color of the car, and its x and y position, width and height.
        # Set the background color and set it to be transparent
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
 
        # Draw the ball (a rectangle!)
        pygame.draw.rect(self.image, color, [0, 0, width, height])
        
        self.velocity = [randint(4,8),randint(-8,8)]
        
        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()
        
    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        
    def bounce(self):
        self.velocity[0] = -self.velocity[0]
        self.velocity[1] = randint(-8,8)
pygame.init()
 
# Define some colors
BLACK = (0,0,0)
WHITE = (255,255,255)
 
# Open a new window
size = (init_msg.width, init_msg.height)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Zekeri Pong")
 
paddleA = Paddle(WHITE, 10, 100)
paddleA.rect.x = init_msg.p1.x
paddleA.rect.y = init_msg.p1.y
 
paddleB = Paddle(WHITE, 10, 100)
paddleB.rect.x = init_msg.p2.x
paddleB.rect.y = init_msg.p2.y
 
ball = Ball(WHITE,10,10)
ball.rect.x = 345
ball.rect.y = 195
 
#This will be a list that will contain all the sprites we intend to use in our game.
all_sprites_list = pygame.sprite.Group()
 
# Add the car to the list of objects
all_sprites_list.add(paddleA)
all_sprites_list.add(paddleB)
all_sprites_list.add(ball)
 
# The loop will carry on until the user exit the game (e.g. clicks the close button).
carryOn = True
 
# The clock will be used to control how fast the screen updates
clock = pygame.time.Clock()
 
#Initialise player scores
scoreA = 0
scoreB = 0

game.ready()
# -------- Main Program Loop -----------
while carryOn:
    # --- Main event loop
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
              carryOn = False # Flag that we are done so we exit this loop
        elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_x: #Pressing the x Key will quit the game
                     carryOn=False
 
    msg = game.refresh()
    #print('(Python) msg is:',dir(msg))
    # update display from fields
    position_p1 = msg.p1
    position_p2 = msg.p2
    position_ball = msg.ball
    result = msg.result
        
    #Moving the paddles when the use uses the arrow keys (player A) or "W/S" keys (player B)
    #This logic should come from c++
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        paddleA.moveUp(5)
    if keys[pygame.K_s]:
        paddleA.moveDown(5)
    if keys[pygame.K_UP]:
        paddleB.moveUp(5)
    if keys[pygame.K_DOWN]:
        paddleB.moveDown(5)    
 
    # --- Game logic should go here
    all_sprites_list.update()
    
    #Check if the ball is bouncing against any of the 4 walls:
    #This logic should come from c++
    if ball.rect.x>=690:
        scoreA+=1
        ball.velocity[0] = -ball.velocity[0]
    if ball.rect.x<=0:
        scoreB+=1
        ball.velocity[0] = -ball.velocity[0]
    if ball.rect.y>490:
        ball.velocity[1] = -ball.velocity[1]
    if ball.rect.y<0:
        ball.velocity[1] = -ball.velocity[1]     
 
    #Detect collisions between the ball and the paddles
    if pygame.sprite.collide_mask(ball, paddleA) or pygame.sprite.collide_mask(ball, paddleB):
      ball.bounce()
    
    # --- Drawing code should go here
    # First, clear the screen to black. 
    screen.fill(BLACK)
    #Draw the net
    pygame.draw.line(screen, WHITE, [349, 0], [349, 500], 5)
    
    #Now let's draw all the sprites in one go. (For now we only have 2 sprites!)
    all_sprites_list.draw(screen) 
 
    #Display scores:
    font = pygame.font.Font(None, 74)
    text = font.render(str(scoreA), 1, WHITE)
    screen.blit(text, (250,10))
    text = font.render(str(scoreB), 1, WHITE)
    screen.blit(text, (420,10))
 
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
     
    # --- Limit to 60 frames per second
    clock.tick(60)
 
#Once we have exited the main program loop we can stop the game engine:
pygame.quit()
sys.exit()
