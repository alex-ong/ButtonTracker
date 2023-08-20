"""
main game class
"""
import asyncio
import pygame
import time
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
    """returns color of button based on state"""
    if state:
        return active
    return GREEN


class Game:
    """main class for game"""

    FPS = 60

    def __init__(self):
        self.starting_steps = readfile()

        pygame.init()
        pygame.display.set_caption("Step trAAAcker")
        logo = pygame.image.load("assets/logo.png")
        pygame.display.set_icon(logo)
        self.screen = pygame.display.set_mode((350, 300))

        self.text_printer = TextPrint()
        self.arrow_state = ArrowState()
        self.joysticks = {}
        self.done = False  # set to true to end.

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

    async def handle_events(self, loop: asyncio.AbstractEventLoop):
        # event handler
        while not self.done:
            await asyncio.sleep(0)
            event = pygame.event.poll()
            if event.type == pygame.NOEVENT:
                continue
            if event.type == pygame.QUIT:  # If user clicked close.
                self.done = True  # Flag that we are done so we exit this loop.
                loop.stop()  # stop asyhcio
            elif event.type == pygame.JOYDEVICEADDED:
                # You need to assign the variable otherwise it gets garbage collected.
                # Once its created (and still in scope), it will create pygame.JOYBUTTONDOWN events
                joystick = pygame.joystick.Joystick(event.device_index)
                self.joysticks[joystick.get_instance_id()] = joystick
            elif event.type == pygame.JOYDEVICEREMOVED:
                del self.joysticks[joystick.get_instance_id()]

            else:  # pass event to arrowtracker
                print(f"an event..., {event.type}")
                self.arrow_state.update(event)

    async def handle_draw(self):
        """
        'thread' to draw to screen
        """
        current_time = 0
        while not self.done:
            # clear screen and draw all elements
            self.screen.fill(BLACK)
            self.draw_arrows()
            self.draw_text()

            # Go ahead and update the screen with what we've drawn.
            pygame.display.flip()

            last_time, current_time = current_time, time.time()
            await asyncio.sleep(1.0 / self.FPS - (current_time - last_time))  # tick
            # print("handle_draw")

    def main(self):
        """
        main function. Runs event handling and drawing in two "threads"
        By threads i mean "asynchronously"
        """

        loop = asyncio.get_event_loop()
        asyncio.ensure_future(self.handle_events(loop))
        asyncio.ensure_future(self.handle_draw())

        loop.run_forever()  # self.handle_events will call loop.stop()

        # write our statistics to file.
        writefile(self.total_steps)

        # Close the window and quit.
        pygame.quit()
