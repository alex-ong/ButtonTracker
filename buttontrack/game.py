"""
main game class
"""
import pygame
from buttontrack.arrowstate import ArrowState
from buttontrack.colors import GREEN, RED, BLUE, BLACK

from buttontrack.stats import readfile, writefile
from buttontrack.text import TextPrint


class PadRect:
    """Class representing rectangles of color for each arrow"""

    PAD = pygame.Rect(0, 0, 150, 150)
    LEFT = pygame.Rect(0, 50, 50, 50)
    DOWN = pygame.Rect(50, 100, 50, 50)
    UP = pygame.Rect(50, 0, 50, 50)
    RIGHT = pygame.Rect(100, 50, 50, 50)


def get_color(active, state):
    """returns color based on state"""
    if state:
        return active
    return GREEN


class Game:
    """main class for game"""

    def __init__(self):
        self.starting_steps = readfile()

        pygame.init()
        pygame.joystick.init()
        pygame.display.set_caption("Step trAAAcker")
        self.screen = pygame.display.set_mode((300, 300))
        self.clock = pygame.time.Clock()
        self.text_printer = TextPrint()
        self.arrow_state = ArrowState()

    @property
    def total_steps(self):
        """return total steps of all time"""
        return self.starting_steps + self.arrow_state.buttons_pressed

    def draw_arrows(self):
        """draws our arrows"""
        pygame.draw.rect(self.screen, GREEN, PadRect.PAD)

        self.draw_arrow(BLUE, self.arrow_state.left, PadRect.LEFT)
        self.draw_arrow(RED, self.arrow_state.down, PadRect.DOWN)
        self.draw_arrow(RED, self.arrow_state.up, PadRect.UP)
        self.draw_arrow(BLUE, self.arrow_state.right, PadRect.RIGHT)

    def draw_arrow(self, active_color, state, rect):
        """draws an arrow to the screen"""
        color = get_color(active_color, state)
        pygame.draw.rect(self.screen, color, rect)

    def draw_text(self):
        """Draws our step count"""
        self.text_printer.reset()
        for _ in range(5):
            self.text_printer.render(self.screen, "")
        self.text_printer.render(
            self.screen,
            "Total Steps:  " + str(self.total_steps).rjust(7),
        )
        self.text_printer.render(
            self.screen,
            "Session Steps:" + str(self.arrow_state.buttons_pressed).rjust(7),
        )

    def refresh_joysticks(self):
        """
        If we plug in our joystick after app start, it needs to be re-initted
        Note that this is deprecated in 2.x if we ever upgrade pygame
        """

        joystick_count = pygame.joystick.get_count()
        for i in range(joystick_count):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()

    def main(self):
        """main loop"""
        # Loop until the user clicks the close button.
        done = False

        while not done:
            for event in pygame.event.get():  # User did something.
                if event.type == pygame.QUIT:  # If user clicked close.
                    done = True  # Flag that we are done so we exit this loop.
                else:  # pass event to arrowtracker
                    self.arrow_state.update(event)

            # clear screen and draw all elements
            self.screen.fill(BLACK)
            self.draw_arrows()
            self.draw_text()

            self.refresh_joysticks()

            # Go ahead and update the screen with what we've drawn.
            pygame.display.flip()

            # Limit to 60 frames per second.
            self.clock.tick(60)

        # write our statistics to file.
        writefile(self.total_steps)

        # Close the window and quit.
        pygame.quit()
