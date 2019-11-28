import random
from functools import lru_cache


class City(object):
    def __init__(self, number: int, weights: list):
        self.number = number
        self.neighbors = weights
        super().__init__()

    @lru_cache(maxsize=None)
    def get_worst(self, illegals):
        """
        """
        worst = 0
        for i, n in enumerate(self.neighbors):
            if i not in illegals:
                worst = n if n > worst else worst
        return worst

    def __repr__(self):
        return f"c:{self.number}"


class GeneticProblem(object):
    """
    """

    def __init__(self, gene_pool: list, len: int):
        self.gene_pool = gene_pool
        self.len = len
        self.population = self.build_population()
        super().__init__()

    def build_population(self, repeative=True):
        """
        """
        population = []
        for i in range(100):
            if repeative:
                p = random.sample(self.gene_pool, k=self.len)
            else:
                p = random.choices(self.gene_pool, k=self.len)
            population.append(p)
        return population

    def fitness_fn(self, sample):
        """
        """
        return 1


class ShopsProblem(GeneticProblem):
    """
    """

    def __init__(self, file: str, len: int):
        self.cities = self.get_cities(file)
        gene_pool = self.get_genes()
        super().__init__(gene_pool=gene_pool, len=len)

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

    def get_genes(self):
        """
        """
        return [city for city in self.cities]

    def fitness_fn(self, sample: list):
        """
        """
        @lru_cache(maxsize=None)
        def fn(shops):
            if len(shops) != len(set(shops)):
                return float('inf')
            worst = 0
            illegals = tuple([b.number for b in shops])
            for city in shops:
                w = city.get_worst(illegals=illegals)
                if w > worst:
                    worst = w
            return worst
        return fn(tuple(sample))

    def build_population(self, repeative=False):
        return super().build_population(repeative=repeative)
