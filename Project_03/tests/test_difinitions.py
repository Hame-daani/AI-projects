from core.definitions import ShopsProblem

problem = ShopsProblem('input.txt',len=3)
cities = problem.cities

def test_get_worst_no_illegals():
    assert cities[0].get_worst(illegals=tuple([])) == 92

def test_get_worst_illegals():
    assert cities[0].get_worst(illegals=tuple([4])) == 88

def test_fitness_zero():
    c0=problem.cities[0]
    c1=problem.cities[1]
    c2=problem.cities[2]
    assert problem.fitness_fn([c0,c1,c2]) == 0

def test_fitness_two():
    c0=problem.cities[7]
    c1=problem.cities[8]
    c2=problem.cities[9]
    assert problem.fitness_fn([c0,c1,c2]) == 2

def test_fitness_repeative():
    c0=problem.cities[7]
    c1=problem.cities[8]
    c2=problem.cities[9]
    assert problem.fitness_fn([c0,c1,c1]) == 0