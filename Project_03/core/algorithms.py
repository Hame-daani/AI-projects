import time
import random
from . import utils


def select(population: list, fitness_fn):
    """
    """
    fits = list(map(fitness_fn, population))
    max_fit = max(fits)
    chances = []
    for fit in fits:
        chance = (max_fit-fit)+1
        if chances:
            chances.append(chance+chances[-1])
        else:
            chances.append(chance)
    p = random.uniform(0, chances[-1])
    x = population(utils.getIndex(population, p))
    p = random.uniform(0, chances[-1])
    y = population(utils.getIndex(population, p))
    return x, y


def reproduce(x: list, y: list):
    """
    """
    n = len(x)
    c = random.randrange(0, n)
    child = x[:c] + y[c:]
    return child


def genetic_algorithm(population: list, fitness_fn, mutate_probability=0.1, fit_target=0, time_target=1):
    """
    """
    start_time = time.time()

    def finished():
        if not fit_target:
            if time.time()-start_time >= time_target:
                return True
        else:
            pass
        return False
    # main func
    while(not finished()):
        new_population = []
        for i in range(len(population)):
            x, y = select(population, fitness_fn)
            child = reproduce(x, y)
            p = random.uniform(0, 1)
            if p < mutate_probability:
                child = mutate(child)
            new_population.append(child)
        population = new_population
    return (population, min(population, key=fitness_fn)
