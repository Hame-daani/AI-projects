import random


class City(object):
    def __init__(self, number: int, weights: list):
        self.number = number
        self.weights = weights
        super().__init__()


class GeneticProblem(object):
    """
    """

    def __init__(self, *args, **kwargs):
        self.gene_pool = kwargs['gene_pool']
        self.len = kwargs['len']
        self.population = self.build_population()
        super().__init__()

    def build_population(self):
        """
        """
        population = []
        for i in range(100):
            p = []
            for l in range(self.len):
                p.append(random.choice(self.gene_pool))
            population.append(p)
        return population


class ShopsProblem(GeneticProblem):
    """
    """

    def __init__(self, *args, **kwargs):
        self.cities = self.get_cities(kwargs['file'])
        kwargs['gene_pool'] = self.get_genes()
        super().__init__(*args, **kwargs)

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
        return [i for i in range(len(self.cities))]
