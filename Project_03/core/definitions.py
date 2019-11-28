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
        return max([weight for index, weight in enumerate(self.neighbors) if index not in illegals])

    def __repr__(self):
        return f"c{self.number}"


class GeneticProblem(object):
    """
    """

    def __init__(self, genes: list, target_len: int, mutate_probability=0.1, fit_target=0, time_target=0, num_genrations=1000, population_num=100):
        self.mutate_probability = mutate_probability
        self.fit_target = fit_target
        self.time_target = time_target
        self.num_generation = num_genrations
        self.genes = genes
        self.target_len = target_len
        self.population_num = population_num
        self.population = self.build_population(population_num)
        super().__init__()

    def build_population(self, num=100, repeative=True):
        """
        """
        population = []
        for i in range(num):
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

    def __init__(self, file: str, target_len: int, mutate_probability=0.1, time_target=0, num_genrations=1000, population_num=100):
        self.cities = self.load_cities(file)
        self.longest = max([city.get_worst() for city in self.cities])
        super().__init__(genes=self.cities, target_len=target_len,
                         mutate_probability=mutate_probability, time_target=time_target, num_genrations=num_genrations, population_num=population_num)

    def load_cities(self, file: str):
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
            illegals = tuple([b.number for b in shops])
            worst = max([city.get_worst(illegals=illegals) for city in shops])
            return self.longest - worst
        return fn(tuple(sample))

    def build_population(self,num=100, repeative=False):
        return super().build_population(num,repeative=repeative)
