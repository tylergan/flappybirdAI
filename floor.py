import pygame
import os


class Floor:
    IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
    VEL = 5
    WIDTH = IMG.get_width()

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        '''We are making the floor move to provide the illusion that flappy bird is moving forward.'''
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        # setup two floors (one outside the window), constantly cycling the two images.
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH  # we will move it back to the right-side of the window once it exits the left-side
        elif self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH
        
    def draw(self, win):
        '''This will draw the two floor images.'''
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))
