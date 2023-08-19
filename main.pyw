import pygame
from buttontrack.text import TextPrint
from buttontrack.arrowstate import ArrowState
from buttontrack.stats import readfile, writefile

# Set this to 1 to enable


# Define some colors.
BLACK = pygame.Color("black")
WHITE = pygame.Color("white")
col1 = [255, 0, 0]
col2 = [0, 0, 255]
col3 = [0, 255, 0]

loadedSteps = readfile()

pygame.init()

# Set the width and height of the screen (width, height).
screen = pygame.display.set_mode((300, 300))

pygame.display.set_caption("My Game")


# Used to manage how fast the screen updates.
clock = pygame.time.Clock()

# Initialize the joysticks.
pygame.joystick.init()

# Get ready to print.
text_print = TextPrint()


pad = pygame.Rect(0, 0, 150, 150)
left = pygame.Rect(0, 50, 50, 50)
down = pygame.Rect(50, 100, 50, 50)
up = pygame.Rect(50, 0, 50, 50)
right = pygame.Rect(100, 50, 50, 50)


def get_color(active, state):
    """returns color based on state"""
    if state:
        return active
    return col3


arrow_state = ArrowState()


def draw_arrows(screen):
    """draws our arrows"""
    pygame.draw.rect(screen, col3, pad)
    pygame.draw.rect(screen, get_color(col2, arrow_state.left), left)
    pygame.draw.rect(screen, get_color(col1, arrow_state.down), down)
    pygame.draw.rect(screen, get_color(col1, arrow_state.up), up)
    pygame.draw.rect(screen, get_color(col2, arrow_state.right), right)


def draw_text(screen, text_print: TextPrint):
    """Draws our step count"""
    for i in range(5):
        text_print.render(screen, "")
    text_print.render(
        screen, "Total Steps:  " + str(loadedSteps + arrow_state.total).rjust(7)
    )
    text_print.render(screen, "Session Steps:" + str(arrow_state.total).rjust(7))
    text_print.reset()


def refresh_joysticks():
    """
    If we plug in our joystick after app start, it needs to be re-initted
    Note that this is deprecated in 2.x if we ever upgrade pygame
    """

    joystick_count = pygame.joystick.get_count()
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()


def main():
    """main loop"""
    # Loop until the user clicks the close button.
    done = False

    while not done:
        for event in pygame.event.get():  # User did something.
            if event.type == pygame.QUIT:  # If user clicked close.
                done = True  # Flag that we are done so we exit this loop.
            else:  # pass event to arrowtracker
                arrow_state.update(event)

        # clear screen and draw all elements
        screen.fill(BLACK)
        draw_arrows(screen)
        draw_text(screen, text_print)

        refresh_joysticks()

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # Limit to 60 frames per second.
        clock.tick(60)

    # write our statistics to file.
    writefile(loadedSteps + arrow_state.total)

    # Close the window and quit.
    pygame.quit()


if __name__ == "__main__":
    main()
