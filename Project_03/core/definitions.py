import random
from functools import lru_cache


class City(object):
    def __init__(self, number: int, weights: list):
        self.number = number
        self.neighbors = weights
        super().__init__()

    @lru_cache(maxsize=None)
    def get_worst(self, illegals=[]):
        """
        """
        worst = 0
        for neigh_index, neigh_weight in enumerate(self.neighbors):
            if neigh_index not in illegals:
                worst = neigh_weight if neigh_weight > worst else worst
        return worst

    def __repr__(self):
        return f"c{self.number}"


class GeneticProblem(object):
    """
    """

    def __init__(self, genes: list, target_len: int, mutate_probability=0.1, fit_target=0, time_target=0, num_genrations=1000):
        self.mutate_probability = mutate_probability
        self.fit_target = fit_target
        self.time_target = time_target
        self.num_generation = num_genrations
        self.genes = genes
        self.target_len = target_len
        self.population = self.build_population()
        super().__init__()

    def build_population(self, repeative=True):
        """
        """
        population = []
        for i in range(100):
            if repeative:
                p = random.choices(self.genes, k=self.target_len)
            else:
                p = random.sample(self.genes, k=self.target_len)
            population.append(p)
        return population

    def fitness_fn(self, sample: list):
        """
        """
        return 1


class ShopsProblem(GeneticProblem):
    """
    """

    def __init__(self, file: str, target_len: int, mutate_probability=0.1, fit_target=0, time_target=0, num_genrations=1000):
        self.cities = self.get_cities(file)
        self.longest = max([city.get_worst() for city in self.cities])
        super().__init__(genes=self.cities, target_len=target_len, mutate_probability=mutate_probability,
                         fit_target=fit_target, time_target=time_target, num_genrations=num_genrations)

    def get_cities(self, file: str):
        """
        """
        cities = []
        with open(file) as f:
            lines = f.readlines()
        f.close()
        for i, line in enumerate(lines):
            row = line.strip('\n').split()
            row = list(map(int, row))
            cities.append(City(number=i, weights=row))
        return cities

    def fitness_fn(self, sample: list):
        """
        """
        @lru_cache(maxsize=None)
        def fn(shops):
            if len(shops) != len(set(shops)):
                return 0
            worst = 0
            illegals = tuple([b.number for b in shops])
            for city in shops:
                w = city.get_worst(illegals=illegals)
                if w > worst:
                    worst = w
            return self.longest - worst
        return fn(tuple(sample))

    def build_population(self, repeative=False):
        return super().build_population(repeative=repeative)
