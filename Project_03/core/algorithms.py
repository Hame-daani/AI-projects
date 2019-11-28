import time
import random
from . import utils
from .definitions import GeneticProblem


def select(population: list, fitness_fn):
    """
    """
    fits = list(map(fitness_fn, population))
    max_fit = max(fits, key=lambda f: -1 if f == float('inf') else f)
    chances = []
    for fit in fits:
        if fit == float('inf'):
            chance = 0
        else:
            chance = (max_fit-fit)+1
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
    c = random.randrange(0, n)
    child = x[:c] + y[c:]
    return child


def mutate(child, gene_pool: list):
    n = len(child)
    g = len(gene_pool)
    c = random.randrange(0, n)
    r = random.randrange(0, g)
    # random.choice(gene_pool)
    new_gene = gene_pool[r]
    return child[:c] + [new_gene] + child[c + 1:]


def genetic_algorithm(population: list, gene_pool: list, fitness_fn, mutate_probability=0.1, fit_target=0, time_target=0, num_gen=1000):
    """
    """
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
        best = min(population, key=fitness_fn)
        print(
            f"Generation {num_generation}: {best} -> {fitness_fn(best)}", end='\r'
        )
    return {'population': population, 'best': min(population, key=fitness_fn), 'weight': fitness_fn(min(population, key=fitness_fn))}


def genetic_serach(problem: GeneticProblem, population=None):
    if not population:
        return genetic_algorithm(population=problem.population, gene_pool=problem.gene_pool, fitness_fn=problem.fitness_fn)
    else:
        return genetic_algorithm(population=population, gene_pool=problem.gene_pool, fitness_fn=problem.fitness_fn)
