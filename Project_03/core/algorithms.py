import time
import random
from . import utils
from .definitions import GeneticProblem


def select(population: list, fitness_fn):
    """
    """
    fits = list(map(fitness_fn, population))
    chances = []
    for i, chance in enumerate(fits):
        for c in range(chance):
            chances.append(i)
    i = random.choice(chances)
    x = population[i]
    i = random.choice(chances)
    y = population[i]
    return x, y


def reproduce(x: list, y: list):
    """
    """
    n = len(x)
    c = random.randint(0, n-1)
    child = x[:c] + y[c:]
    return child


def mutate(child, genes: list):
    n = len(child)
    c = random.randint(0, n-1)
    new_gene = random.choice(genes)
    return child[:c] + [new_gene] + child[c + 1:]


def genetic_algorithm(problem: GeneticProblem, population: list = None):
    """
    """
    all_best_fit = float('inf')
    all_best = []
    if not population:
        population = problem.population
    num_gen = 0

    start_time = time.time()

    def finished():
        if problem.time_target:
            if time.time()-start_time >= problem.time_target:
                return True
        if problem.fit_target:
            pass
        if problem.num_generation:
            if problem.num_generation < num_gen:
                return True
        return False
    # main func
    while(not finished()):
        num_gen += 1
        new_population = []
        for i in range(len(population)):
            x, y = select(population, problem.fitness_fn)
            child = reproduce(x, y)
            p = random.uniform(0, 1)
            if p < problem.mutate_probability:
                child = mutate(child, problem.genes)
            new_population.append(child)
        population = new_population
        best = max(population, key=problem.fitness_fn)
        best_fit = problem.fitness_fn(best)
        if all_best_fit >= best_fit:
            all_best_fit = best_fit
            all_best = best
        print(
            f"Generation {num_gen}:{best_fit} | All Best = {all_best_fit} -> {all_best[:20]}", end='\r'
        )
    return {'population': population, 'best': best, 'fit': best_fit}
