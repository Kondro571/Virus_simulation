import copy
class Memento:
    def __init__(self, dimensions, population_list):
        self.dimensions = dimensions
        self.list = copy.deepcopy(population_list)
