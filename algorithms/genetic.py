import random
import pandas as pd

from .base import BaseAlgorithm
from utils import get_total_route_time

POPULATION_SIZE = 5
NUMBER_GENERATIONS = 2
ELIT_SIZE = 2
MUTATION_RATE = 0.01


class Genetic(BaseAlgorithm):
    def __init__(self, map, ncars_by_street):
        super().__init__(map, ncars_by_street)
        self.pop = pd.DataFrame()

    def get_route(self, source, dest, path=[]):
        initial_population = self.get_initial_population(source, dest)
        self.pop = self.rank_routes(initial_population)

        for i in range(0, NUMBER_GENERATIONS):
            self.pop = self.next_generation()

        return self.pop.sort_values("cost", ascending=True)['route'].iloc[0]

    def next_generation(self):
        mathingpool = self.matching_pool(ELIT_SIZE)
        mutate_population = self.get_mutate_population(mathingpool, MUTATION_RATE)
        return mutate_population

    @staticmethod
    def breed(parent1, parent2):
        random_street = random.choice(parent1)
        child = parent1
        if random_street in parent2:
            child = parent1[:parent1.index(random_street)] + parent2[parent2.index(random_street):]
        return child

    def matching_pool(self, elit_size):
        return self.pop.head(elit_size)

    def get_mutate_population(self, mathingpool, mutate_rate):
        if mathingpool.shape[1] <= 2:
            # impossible create a new generation
            return mathingpool
        mutate_population = []
        for i in range(mathingpool.shape[1]-1):
            if random.random() < mutate_rate:
                new_route = self.breed(mathingpool['route'].iloc[i], mathingpool['route'].iloc[i+1])['route']
                mutate_population.append(new_route)
            else:
                mutate_population.append(mathingpool['route'].iloc[i])
        return self.rank_routes(mutate_population)

    def get_initial_population(self, source, dest):
        possible_paths = self.map.find_all_possible_paths(source, dest)
        return random.sample(possible_paths, POPULATION_SIZE)

    def rank_routes(self, routes):
        costs = list(map(lambda x: get_total_route_time(x, self.ncars_by_street), routes))
        routes_cost = pd.DataFrame({"route": routes, "cost": costs})
        return routes_cost.sort_values("cost", ascending=True)
