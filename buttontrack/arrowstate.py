"""
Class to keep button state
"""

from dataclasses import asdict, dataclass, field
import os

import pygame
from buttontrack.time import current_ts

# Set this to 1 to enable joystick working in background.
os.environ["SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS"] = "1"

LEFT = 0
DOWN = 1
UP = 2
RIGHT = 3


@dataclass
class StepInterval:
    """Simple class representing a set of steps and when they took place"""

    start_ts: int = field(default_factory=current_ts)
    end_ts: int = field(default_factory=current_ts)
    num_steps: int = 0

    def export(self):
        """exports as dictionary for use with api's in json format"""
        return asdict(self)

    def add_step(self, num=1):
        """adds a step to the inteval"""
        self.num_steps += num
        self.end_ts = current_ts()


class ArrowState:
    """Class that keeps track of how many arrows you've pressed"""

    def __init__(self):
        self.up = True
        self.down = True
        self.left = True
        self.right = True
        self._step_interval = StepInterval()

    def create_new_interval(self) -> StepInterval:
        """return current step interval, then create a new one"""
        self._step_interval.end_ts = current_ts()
        result = self._step_interval
        self._step_interval = StepInterval()
        return result

    @property
    def step_count(self):
        """return current steps in interval"""
        return self._step_interval.num_steps

    @property
    def last_updated(self):
        """return last time we added a step in seconds since epoch"""
        return self._step_interval.end_ts

    @property
    def buttons_pressed(self):
        """returns how many buttons in current step_session"""
        return self._step_interval.num_steps

    @property
    def is_neutral(self):
        """returns if no buttons are held down"""
        for button in [self.left, self.down, self.right, self.up]:
            if button:
                return False
        return True

    def update(self, event):
        """pleb code instead of a nice map..."""
        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == LEFT:
                self.left = True
            elif event.button == DOWN:
                self.down = True
            elif event.button == RIGHT:
                self.right = True
            elif event.button == UP:
                self.up = True
            else:
                return
            self._step_interval.add_step()
        elif event.type == pygame.JOYBUTTONUP:
            if event.button == LEFT:
                self.left = False
            elif event.button == DOWN:
                self.down = False
            elif event.button == RIGHT:
                self.right = False
            elif event.button == UP:
                self.up = False
        elif event.type == pygame.KEYDOWN:
            if event.key == 97:  # a
                self.left = True
            elif event.key == 115:  # s
                self.down = True
            elif event.key == 100:  # d
                self.right = True
            elif event.key == 119:  # f
                self.up = True
            else:
                return  # don't add one to count
            self._step_interval.add_step()
        elif event.type == pygame.KEYUP:
            if event.key == 97:  # a
                self.left = False
            elif event.key == 115:  # s
                self.down = False
            elif event.key == 100:  # d
                self.right = False
            elif event.key == 119:  # f
                self.up = False
