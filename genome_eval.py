import pygame
import neat
from bird import Bird
from pipe import Pipe
from floor import Floor
from draw_window import draw_window

pygame.font.init()


def eval_genomes(genomes, config):
    '''This function contains both logic in the game and the NEAT algorithm.'''
    global gen
    gen += 1
    score = 0

    birds = []
    nets = []
    ge = []

    # set up the neural network for the genome
    for _, genome in genomes:  # genomes contains tuples (ID, Object)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        birds.append(Bird(230, 350))
        ge.append(genome)
        genome.fitness = 0

    # setup game.
    floor = Floor(730)
    pipes = [Pipe(600)]
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    # main
    while len(birds) > 0:
        clock.tick(30)  # will conduct X number of ticks every second

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():  # if we pass the first pipe, focus on the next coming second set of pipes
                pipe_ind = 1

        for x, bird in enumerate(birds):
            ge[x].fitness += 0.1  # reward the bird for moving forward
            bird.move()

            # send bird location, top pipe location and bottom pipe location and determine from network whether to jump or not (returns a list)
            output = nets[x].activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))

            if output[0] > 0.5:
                bird.jump()

        add_pipe = False
        to_remove = []
        for pipe in pipes:
            for x, bird in enumerate(birds):
                if pipe.collide(bird):
                    ge[x].fitness -= 1  # punish birds that hit the pipe
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)

                if not pipe.passed and pipe.x < bird.x:  # if the bird passes the pipe
                    pipe.passed = True
                    add_pipe = True

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:  # pipe will be removed if it exits screen
                to_remove.append(pipe)

            pipe.move()

        if add_pipe:
            score += 1
            for genome in ge:
                genome.fitness += 5  # reward birds that makes it through the pipe

            pipes.append(Pipe(600))

        # remove any pipes that flappy bird has passed
        for pipe in to_remove:
            pipes.remove(pipe)

        for x, bird in enumerate(birds):
            if bird.y + bird.img.get_height() >= 730 or bird.y < 0:  # if the bird touches the ground
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)

        floor.move()

        draw_window(win, birds, pipes, floor, score, gen)

        # if score > 50:  # if we have found a bird the can comeplete up to 150, we found a good bird.
        #     break


# set dimensions of screen
WIN_WIDTH = 500
WIN_HEIGHT = 800

gen = 0
