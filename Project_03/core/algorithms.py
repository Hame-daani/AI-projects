import time
import random


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
            x = select(population, fitness_fn)
            y = select(population, fitness_fn)
            child = reproduce(x, y)
            p = random.uniform(0, 1)
            if p < mutate_probability:
                child = mutate(child)
            new_population.append(child)
        population = new_population
    return (population, min(population, key=fitness_fn)
