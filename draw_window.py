import pygame
import os


def draw_window(win, birds, pipes, floor, score, gen):
    '''Method that will display all everything onto the pygame window.'''
    BG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))
    STAT_FONT = pygame.font.SysFont("comicsans", 50)
    win.blit(BG, (0, 0))

    for pipe in pipes:
        pipe.draw(win)

    # draw the score
    text = STAT_FONT.render("Score: {}".format(score), 1, (255, 255, 255))
    win.blit(text, (500 - 10 - text.get_width(), 10))  # width = 500

    text = STAT_FONT.render("Gen: {}".format(gen), 1, (255, 255, 255))
    win.blit(text, (10, 10))

    floor.draw(win)

    for bird in birds:
        bird.draw(win)

    pygame.display.update()
