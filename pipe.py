import pygame
import os
import random


class Pipe:
    IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
    GAP = 200
    VEL = 5

    def __init__(self, x):
        self.x = x
        self.y = 0

        self.top = 0  # top pipe starting position.
        self.bottom = 0  # bottom pipe starting position.
        self.PIPE_TOP = pygame.transform.flip(self.IMG, False, True)  # flip the image upside down.
        self.PIPE_BOTTOM = self.IMG

        self.passed = False
        self.set_height()
 
    def set_height(self):
        '''This instance method has each pipe set at a different height.'''
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        '''This instance method moves the pipes to the left.'''
        self.x -= self.VEL

    def draw(self, win):
        '''This instance method draws the pipes.'''
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird):
        '''This instance method determines whether there is a collision between flappy bird and the pipe. The technique used is called masking.'''
        # masks used for collision --> see documentation for more
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        # checking for collision on top or bottom pipe with flappy bird.
        b_collide = bird_mask.overlap(bottom_mask, bottom_offset)  # retrun None if no overlap
        t_collide = bird_mask.overlap(top_mask, top_offset)

        return True if b_collide or t_collide else False
