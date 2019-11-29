import time
import random
from . import utils
from .definitions import GeneticProblem


def genetic_algorithm(problem: GeneticProblem, population: list = None):
    """
    """
    all_best_fit = 0
    all_best = []
    if not population:
        population = problem.population
    num_gen = 0
    start_time = time.time()

    def finished():
        if problem.time_target:
            if time.time()-start_time >= problem.time_target:
                print("\nTimes Up!")
                return True
        if problem.fit_target:
            if all_best_fit == problem.fit_target:
                print("\nGet There!")
                return True
        if problem.num_generation:
            if problem.num_generation <= num_gen:
                print("\nGenerations Exceed!")
                return True
        return False
    # main func
    while(not finished()):
        num_gen += 1
        new_population = []
        for i in range(len(population)):
            x, y = problem.select(population, problem.fitness_fn)
            child = problem.reproduce(x, y)
            # while(not problem.isValid(child)):
            #     problem.fitness_fn(child)
            #     x, y = select(population, problem.fitness_fn)
            #     child = reproduce(x, y)
            p = random.uniform(0, 1)
            if p < problem.mutate_probability:
                child = problem.mutate(child, problem.genes)
            new_population.append(child)
        population = new_population
        best = max(population, key=problem.fitness_fn)
        best_fit = problem.fitness_fn(best)
        if all_best_fit <= best_fit:
            all_best_fit = best_fit
            all_best = best
        print(
            f"Gen {num_gen}:{problem.longest - best_fit} | Best={problem.longest - all_best_fit}->{all_best[:20]}", end='\r'
        )
    return {'population': population, 'best': all_best, 'fit': all_best_fit}
