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
            print("Joystick button pressed.")
            print(event)            
        elif event.type == pygame.JOYBUTTONUP:
            print("Joystick button released.")
            print(event)
            
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
            