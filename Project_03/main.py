from core.algorithms import genetic_algorithm, hill_climbing, random_restart_hill_climbing
from core.definitions import ShopsProblem, HillClimbingProblem, StochasticHillClimbingProblem, FirstChoiceHillClimbingProblem
import sys


# problem = ShopsProblem(file="input2.txt", target_len=30, mutate_probability=0.1, time_target=120,
#                        fit_target=0, num_genrations=10000, population_num=30)

# result = genetic_algorithm(problem)
# print(f"Best: {result['best']}")
# print(f"Weight: {result['fit']}")

# shops = []
# for i in [52, 35, 33, 81, 61, 12, 98, 17, 38, 44, 60, 84, 75, 31, 34, 70, 83, 88, 62, 64, 20, 26, 39, 47, 46, 90, 19, 41, 28, 97]:
#     shops.append(problem.cities[i])
# print(problem.fitness_fn(shops))


problem = HillClimbingProblem(file="input2.txt", target_len=30,steps=10)
# problem = FirstChoiceHillClimbingProblem(file="input2.txt", target_len=30, steps=10)
# problem = StochasticHillClimbingProblem(file="input2.txt", target_len=30,steps=10)
print(random_restart_hill_climbing(problem).state)


# Best: [c69, c52, c89, c14, c81, c64, c83, c92, c84, c50, c34, c97, c44, c73, c19, c42, c2, c59, c61, c37, c39, c87, c20, c11, c58, c9, c54, c48, c85, c28]
# Weight: 30
