import random


class GeneticProblem(object):
    """
    """

    def __init__(self, gene_pool: list, len: int):
        self.gene_pool = gene_pool
        self.len = len
        self.population = self.build_population()

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

    def __init__(self, file: str, len: int):
        self.weights = self.build_weights(file)
        gene_pool = self.get_genes()
        super().__init__(gene_pool, len)

    def build_weights(self, file: str):
        """
        """
        weights = []
        with open(file) as f:
            lines = f.readlines()
        f.close()
        for line in lines:
            row = line.strip('\n').split()
            weights.append(row)
        return weights

    def get_genes(self):
        """
        """
        return [i for i in range(len(self.weights))]
