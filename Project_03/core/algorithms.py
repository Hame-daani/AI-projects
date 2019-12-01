import time
import random
from . import utils
from .definitions import GeneticProblem


def genetic_algorithm(problem: GeneticProblem):
    """
    """
    all_best_fit = 0
    all_best = []
    num_gen = 0
    start_time = time.time()

    def finished():
        if problem.time_target:
            if time.time()-start_time >= problem.time_target:
                print("\nTimes Up!")
                return True
        if problem.fit_target:
            if all_best_fit >= problem.fit_target:
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
        problem.evaluate()
        for i in range(len(problem.population)):
            x, y = problem.select(problem.population)
            child = problem.reproduce(x, y)
            while(not problem.isValid(child)):
                x, y = problem.select(problem.population)
                child = problem.reproduce(x, y)
            p = random.uniform(0, 1)
            if p < problem.mutate_probability:
                child = problem.mutate(child)
            new_population.append(child)
        best_fit = max(problem.fits)
        if all_best_fit < best_fit:
            all_best_fit = best_fit
            all_best = problem.population[problem.fits.index(best_fit)]
        problem.population = new_population
        print(
            f"Generation {num_gen}:Best {problem.longest - best_fit} | All Best = {problem.longest - all_best_fit} -> {all_best[:15]}", end='\r'
        )
    return {'population': problem.population, 'best': all_best, 'fit': all_best_fit}
