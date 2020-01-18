from .core.algorithms import (genetic_algorithm, hill_climbing,
                              random_restart_hill_climbing)
from .core.definitions import (FirstChoiceHillClimbingProblem,
                               HillClimbingProblem, ShopsProblem,
                               StochasticHillClimbingProblem)

problem = ShopsProblem(file="input2.txt", target_len=30, mutate_probability=0.1, time_target=120,
                       fit_target=0, num_genrations=10000, population_num=30)

result = genetic_algorithm(problem)
print(f"Best: {result['best']}")
print(f"Weight: {result['fit']}")


problem = HillClimbingProblem(file="input2.txt", target_len=30,steps=10)
# problem = FirstChoiceHillClimbingProblem(file="input2.txt", target_len=30, steps=10)
# problem = StochasticHillClimbingProblem(file="input2.txt", target_len=30,steps=10)
# print(random_restart_hill_climbing(problem).state)
