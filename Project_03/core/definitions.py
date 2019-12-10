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
            d.append(self.neighbors[city.number])
        return min(d)

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
        raise NotImplementedError

    def evaluate(self):
        fits = list(map(self.fitness_fn, self.population))
        self.fits = fits
        self.get_chances()

    def get_chances(self):
        raise NotImplementedError

    def isValid(self, sample):
        raise NotImplementedError

    def select(self):
        """
        """
        draw = nprand.choice(self.population_num, 2, p=self.chances)
        x = self.population[draw[0]]
        y = self.population[draw[1]]
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
        new_child = child[:c] + [new_gene] + child[c + 1:]
        while not self.isValid(child):
            c = random.randint(0, n-1)
            new_gene = random.choice(self.genes)
            new_child = child[:c] + [new_gene] + child[c + 1:]
        return new_child


class ShopsProblem(GeneticProblem):
    """
    """

    def __init__(self, file: str, target_len: int, mutate_probability=0.1, time_target=0, fit_target=0, num_genrations=1000, population_num=100):
        self.cities = self.load_cities(file)
        super().__init__(genes=self.cities, target_len=target_len,
                         mutate_probability=mutate_probability, time_target=time_target, num_genrations=num_genrations, population_num=population_num,
                         fit_target=fit_target)

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
            w = []
            for city in self.cities:
                w.append(city.get_closest(shops))
            worst = max(w)
            return worst
        # main func
        return fn(tuple(sample))

    def init_population(self, num=100, repeative=False):
        return super().init_population(num, repeative=repeative)

    def get_chances(self):
        f_max = max(self.fits)
        fits = [f_max-f for f in self.fits]
        f_sum = sum(fits)
        if f_sum:
            self.chances = [f/f_sum for f in fits]
        else:
            self.chances = [1/self.population_num]*self.population_num


class Node(object):
    def __init__(self, state):
        self.state = state
        super().__init__()

    def expand(self, problem):
        neighbors = []
        for i in range(len(self.state)):
            for city in problem.cities:
                if city not in self.state:
                    neighbors.append(Node(
                        self.state[:i]+[city]+self.state[i+1:]))
        return neighbors


class HillClimbingProblem(object):
    def __init__(self, file: str, target_len: int):
        self.cities = self.load_cities(file)
        self.target_len = target_len
        super().__init__()

    def initial_state(self):
        return random.sample(self.cities, k=self.target_len)

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

    def value(self, node):
        """
        """
        @lru_cache(maxsize=None)
        def fn(shops):
            w = []
            for city in self.cities:
                w.append(city.get_closest(shops))
            worst = max(w)
            return worst
        # main func
        return fn(tuple(node.state))

    def select_neighbor(self, node: Node):
        neighbors = node.expand(self)
        m = min(neighbors, key=self.value)
        return m
