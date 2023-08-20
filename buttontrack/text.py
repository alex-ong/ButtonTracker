"""
simple text printing; in screenspace
"""
import pygame
from buttontrack.colors import WHITE


# This is a simple class that will help us print to the screen.


class TextPrint(object):
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font("assets/PressStartK_proper8.ttf", 16)

    def render(self, screen, text):
        """render our text to screen, then go to next line"""
        font_surface = self.font.render(text, False, WHITE)
        screen.blit(font_surface, (self.x, self.y))
        self.y += self.line_height

    def reset(self):
        """reset where we render to"""
        self.x = 10
        self.y = 10
        self.line_height = 30

    def indent(self):
        self.x += 10

    def unindent(self):
        self.x -= 10
