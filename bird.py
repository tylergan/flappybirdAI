import pygame
import os


class Bird:
    BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))), 
                 pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))), 
                 pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]
    MAX_ROTATION = 25  # max amount it will tilt when going up
    ROT_VEL = 20  # how much the bird  will rotate each frame

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0  # bird will start off flat
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.BIRD_IMGS[0]

    def jump(self):
        '''Method that will make flappy bird jump.'''
        self.vel = -10.5  # to go up by 10.5 pixels
        self.tick_count = 0
        self.height = self.y

    def move(self):
        '''Method that will simply move the bird constantly down (unlessthe jump method is used, changing the displacement equation) and will tilt the bird.'''
        self.tick_count += 1
        displacement = self.vel * self.tick_count + 1.5 * self.tick_count**2  # displacement equation where time = tick_count and acceleration = 3

        if displacement >= 16:
            displacement = 16
        elif displacement < 0:  # if we are moving upwards, move up a bit more for smoother jump
            displacement -= 2

        self.y += displacement  # make bird fall down

        # tilting the bird
        if displacement < 0 or self.y < self.height + 50:  # if the bird is above the starting neutral positon, tilt upwards
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def draw(self, win):
        '''Method that will draw the bird.'''
        # transitioning bird states
        self.img_count += 0.08
        img_index = int(self.img_count % len(self.BIRD_IMGS))
        self.img = self.BIRD_IMGS[img_index]

        if self.tilt <= -80:  # if the bird is falling down, it should not be flapping its wings
            self.img = self.BIRD_IMGS[1]
            self.img_count = 1

        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)  # rotate the image around the center
        win.blit(rotated_image, new_rect.topleft)  # rotate the image
    
    def get_mask(self):
        return pygame.mask.from_surface(self.img)
