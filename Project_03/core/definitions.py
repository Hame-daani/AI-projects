import random
from functools import lru_cache
import numpy.random as nprand


class City(object):
    def __init__(self, number: int, weights: list):
        self.number = number
        self.neighbors = weights
        super().__init__()

    @lru_cache(maxsize=None)
    def get_closest(self, shops: tuple):
        """
        """
        d = []
        for city in shops:
            d.append(self.neighbors[city])
        return min(d)

    def __repr__(self):
        return f"{self.number}"


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
        self.fits = []
        self.population = self.init_population(population_num)
        super().__init__()

    def init_population(self, num=100, repeative=True):
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
        return NotImplementedError

    def evaluate(self):
        fits = list(map(self.fitness_fn, self.population))
        self.fits = fits

    def select(self, population: list):
        """
        """
        f_sum = sum(self.fits)
        chances = [f/f_sum for f in self.fits]
        draw = nprand.choice(self.population_num, 2, p=chances)
        x = population[draw[0]]
        y = population[draw[1]]
        return (x, y)

    def reproduce(self, x: list, y: list):
        """
        """
        n = len(x)
        c = random.randint(0, n-1)
        child = x[:c] + y[c:]
        return child

    def mutate(self, child):
        n = len(child)
        c = random.randint(0, n-1)
        new_gene = random.choice(self.genes)
        return child[:c] + [new_gene] + child[c + 1:]


class ShopsProblem(GeneticProblem):
    """
    """

    def __init__(self, file: str, target_len: int, mutate_probability=0.1, time_target=0, fit_target=0, num_genrations=1000, population_num=100):
        self.cities = self.load_cities(file)
        self.longest = max([max(city.neighbors) for city in self.cities])
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

    def isValid(self, sample):
        if len(sample) != len(set(sample)):
            return False
        return True

    def fitness_fn(self, sample: list):
        """
        """
        @lru_cache(maxsize=None)
        def fn(shops):
            d = []
            for shop_index in shops:
                d.append(self.cities[shop_index].neighbors)
            w = []
            for i in range(len(self.cities)):
                j = [s[i] for s in d]
                if j.count(0):
                    continue
                best = min(j)
                w.append(best)
            worst = max(w)
            return self.longest - worst
        # main func
        if len(sample) != len(set(sample)):
            return 0
        shops = [b.number for b in sample]
        return fn(tuple(shops))

    def init_population(self, num=100, repeative=False):
        return super().init_population(num, repeative=repeative)
