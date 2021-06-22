import neat
import os
# import pickle5 as pickle
from genome_eval import eval_genomes


def run(config_path):
    '''This function runs the entire program.'''
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)

    population = neat.Population(config)

    # provide statistics on each generation to stdout
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    winner = population.run(eval_genomes, 50)  # set fitness function and runs eval_genome
    print('\nBest genome:\n{!s}'.format(winner))

    # pickle.dump(winner, open("best.pickle", "wb"))  # you can save the bird in a file


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "AI_config.txt")
    run(config_path)
