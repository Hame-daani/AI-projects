from core.algorithms import genetic_algorithm
from core.definitions import ShopsProblem
import sys

problem = ShopsProblem(file="input2.txt", target_len=30, mutate_probability=0.01,
                       time_target=60, num_genrations=100000, population_num=20)

# shops = []
# for i in [2, 4, 99, 14, 89, 20, 5, 61, 65, 69, 92, 41, 28, 39, 19, 81, 97, 57, 48, 52, 37, 78, 95, 84, 70, 29, 54, 83, 1, 47]:
#     shops.append(problem.cities[i])
# print(problem.fitness_fn(shops))

result = genetic_algorithm(problem)
print(f"Best: {result['best']}")
print(f"Weight: {result['fit']}")

# Best: [c2, c4, c99, c14, c89, c20, c5, c61, c65, c69, c92, c41, c28, c39, c19, c81, c97, c57, c48, c52, c37, c78, c95, c84, c70, c29, c54, c83, c1, c47]
# Weight: 37

# Best: [c75, c94, c38, c52, c90, c97, c28, c67, c27, c37, c39, c79, c92, c61, c48, c56, c63, c34, c12, c4, c17, c72, c83, c36, c73, c9, c24, c13, c14, c18]
# Weight: 34

