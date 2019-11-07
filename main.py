from TextPrint import TextPrint
from ArrowTracker import ArrowTracker
import pygame
from stats import readfile, writefile

    
# Define some colors.
BLACK = pygame.Color('black')
WHITE = pygame.Color('white')
col1 = [255,0,0]
col2 = [0,0,255]
col3 = [0,255,0] 

loadedSteps = readfile()

pygame.init()

# Set the width and height of the screen (width, height).
screen = pygame.display.set_mode((300, 300))

pygame.display.set_caption("My Game")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates.
clock = pygame.time.Clock()

# Initialize the joysticks.
pygame.joystick.init()

# Get ready to print.
textPrint = TextPrint()


pad = pygame.Rect(0,0,150,150)
left =  pygame.Rect(0, 50, 50, 50)
down =  pygame.Rect(50, 100, 50, 50)
up  =  pygame.Rect(50, 0, 50, 50)
right =  pygame.Rect(100, 50, 50, 50)

   
at = ArrowTracker()

# -------- Main Program Loop -----------
while not done:    
    for event in pygame.event.get(): # User did something.
        if event.type == pygame.QUIT: # If user clicked close.
            done = True # Flag that we are done so we exit this loop.
        else: #pass event to arrowtracker
            at.update(event)
    #
    # DRAWING STEP
    #
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(BLACK)
    pygame.draw.rect(screen, col3, pad)
    pygame.draw.rect(screen, col2 if at.left else col3, left)
    pygame.draw.rect(screen, col1 if at.down else col3, down)
    pygame.draw.rect(screen, col1 if at.up else col3, up)
    pygame.draw.rect(screen, col2 if at.right else col3, right)
    for i in range(5):
        textPrint.tprint(screen, "")
    textPrint.tprint(screen, "Total Steps:  " +str(loadedSteps + at.total).rjust(7))
    textPrint.tprint(screen, "Session Steps:" +str(at.total).rjust(7))
    textPrint.reset()

    #
    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
    #
    joystick_count = pygame.joystick.get_count()
    # For each joystick:
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # Limit to 20 frames per second.
    clock.tick(60)

#write our statistics to file.
writefile(loadedSteps+at.total)

# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()