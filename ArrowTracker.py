import pygame
class ArrowTracker():
    def __init__(self):
        self.up = True
        self.down = True
        self.left = True
        self.right = True
        self.total = 0
        
    def update(self, event):        
        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == 0: #left
                self.left = True
            elif event.button == 1: #down
                self.down = True
            elif event.button == 2: #right
                self.right = True
            elif event.button == 3: #down
                self.up = True
        elif event.type == pygame.JOYBUTTONUP:
            if event.button == 0: #left
                self.left = False
            elif event.button == 1: #down
                self.down = False
            elif event.button == 2: #right
                self.right = False
            elif event.button == 3: #down
                self.up = False
        elif event.type == pygame.KEYDOWN:
            if event.key == 97: #a
                self.left = True
            elif event.key == 115: #s
                self.down = True
            elif event.key  == 100: #d
                self.right = True
            elif event.key == 119: #f
                self.up = True
            else:
                return #don't add one to count
            self.total += 1
            
        elif event.type == pygame.KEYUP:            
            if event.key == 97: #a
                self.left = False
            elif event.key == 115: #s
                self.down = False
            elif event.key  == 100: #d
                self.right = False
            elif event.key == 119: #f
                self.up = False
            