import random


class City(object):
    def __init__(self, number: int, weights: list):
        self.number = number
        self.neighbors = weights
        super().__init__()

    def get_worst(self, budies):
        """
        """
        worst = 0
        for i, n in enumerate(self.neighbors):
            if all(i != b.number for b in budies):
                worst = n if n > worst else worst
        return worst

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
            p = []
            for l in range(self.len):
                if repeative:
                    p.append(random.choice(self.gene_pool))
                else:
                    r = random.choice(self.gene_pool)
                    while r in p:
                        r = random.choice(self.gene_pool)
                    p.append(r)
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

    def fitness_fn(self, shops: list):
        """
        """
        if len(shops) != len(set(shops)):
            return float('inf')
        worst = 0
        for city in shops:
            w = city.get_worst(budies=shops)
            if w > worst:
                worst = w
        return worst

    def build_population(self, repeative=False):
        return super().build_population(repeative=repeative)
