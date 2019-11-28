import time
import random
from . import utils
from .definitions import GeneticProblem


def select(population: list, fitness_fn):
    """
    """
    fits = list(map(fitness_fn, population))
    chances = []
    for fit in fits:
        chance = fit
        if chances:
            chances.append(chance+chances[-1])
        else:
            chances.append(chance)
    p = random.uniform(0, chances[-1])
    x = population[utils.getIndex(chances, p)]
    p = random.uniform(0, chances[-1])
    y = population[utils.getIndex(chances, p)]
    return x, y


def reproduce(x: list, y: list):
    """
    """
    n = len(x)
    c = random.randint(0, n-1)
    child = x[:c] + y[c:]
    return child


def mutate(child, gene_pool: list):
    n = len(child)
    c = random.randint(0, n-1)
    new_gene = random.choice(gene_pool)
    return child[:c] + [new_gene] + child[c + 1:]


def genetic_algorithm(problem: GeneticProblem, population: list = None, mutate_probability=0.1, fit_target=0, time_target=0, num_gen=1000):
    """
    """
    all_best = float('inf')
    if not population:
        population = problem.population
    fitness_fn = problem.fitness_fn
    gene_pool = problem.gene_pool
    start_time = time.time()
    num_generation = 0

    def finished():
        if time_target:
            if time.time()-start_time >= time_target:
                return True
        elif fit_target:
            pass
        elif num_gen:
            if num_generation > num_gen:
                return True
        return False
    # main func
    while(not finished()):
        num_generation += 1
        new_population = []
        for i in range(len(population)):
            x, y = select(population, fitness_fn)
            child = reproduce(x, y)
            p = random.uniform(0, 1)
            if p < mutate_probability:
                child = mutate(child, gene_pool)
            new_population.append(child)
        population = new_population
        best = max(population, key=fitness_fn)
        best_fit = problem.longest - fitness_fn(best)
        all_best = best_fit if all_best > best_fit else all_best
        print(
            f"best: {all_best} - Generation {num_generation}: {best_fit} -> {best[:20]}", end='\r'
        )
    return {'population': population, 'best': best, 'weight': best_fit}


def genetic_serach(problem: GeneticProblem, population=None):
    if not population:
        return genetic_algorithm(problem=problem, population=problem.population, gene_pool=problem.gene_pool, fitness_fn=problem.fitness_fn)
    else:
        return genetic_algorithm(population=population, gene_pool=problem.gene_pool, fitness_fn=problem.fitness_fn)
