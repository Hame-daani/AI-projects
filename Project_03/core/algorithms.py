import time
import random
from . import utils
from .definitions import GeneticProblem, HillClimbingProblem, Node, StochasticHillClimbingProblem


def genetic_algorithm(problem: GeneticProblem):
    """
    """
    all_best_fit = float('inf')
    num_gen = 0
    start_time = time.time()

    def finished():
        if problem.time_target:
            if time.time()-start_time >= problem.time_target:
                print("\nTimes Up!")
                return True
        if problem.fit_target:
            if all_best_fit <= problem.fit_target:
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
            x, y = problem.select()
            child = problem.reproduce(x, y)
            while(not problem.isValid(child)):
                x, y = problem.select()
                child = problem.reproduce(x, y)
            p = random.uniform(0, 1)
            if p < problem.mutate_probability:
                child = problem.mutate(child)
            new_population.append(child)
        best_fit = min(problem.fits)
        best = problem.population[problem.fits.index(best_fit)]
        if all_best_fit > best_fit:
            all_best_fit = best_fit
            all_best = best
        problem.population = new_population
        print(
            f"Gen {num_gen} : {best_fit}->{best[:25]}", end='\r'
        )
    return {'population': problem.population, 'best': all_best, 'fit': all_best_fit}


def hill_climbing(problem: HillClimbingProblem, steps=10):
    for i in range(steps):
        print(f"Start {i+1} Time.")
        current = Node(problem.initial_state())
        while True:
            neighbor = problem.select_neighbor(current)
            if problem.value(neighbor) >= problem.value(current):
                break
            current = neighbor
            print(f"{problem.value(current)} -> {current.state}")
    return current.state


def stochastic_hill_climbing(problem: StochasticHillClimbingProblem, steps=50):
    for i in range(steps):
        print(f"{i+1} Time.")
        current = Node(problem.initial_state())
        neighbor = problem.select_neighbor(current)
        current = neighbor
        print(f"{problem.value(current)} -> {current.state}")
    return current.state
