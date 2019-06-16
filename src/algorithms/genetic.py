import random
import pandas as pd

from .base import BaseAlgorithm
from utils import get_total_route_time

POPULATION_SIZE = 2
NUMBER_GENERATIONS = 3


class Genetic(BaseAlgorithm):
    def __init__(self, map, ncars_by_street):
        super().__init__(map, ncars_by_street)

    def get_route(self, source, dest, path=[]):
        pop = self.initial_population(source, dest)

        # for i in range(0, NUMBER_GENERATIONS):
        #     pop = next_generation(pop)

        pop_cost = self.rank_routes(pop)
        return pop_cost.sort_values("cost", ascending=True)['route'].iloc[0]

    def initial_population(self, source, dest):
        possible_paths = self.map.find_all_possible_paths(source, dest)
        return random.sample(possible_paths, POPULATION_SIZE)

    def rank_routes(self, routes):
        costs = list(map(lambda x: get_total_route_time(x, self.ncars_by_street), routes))
        routes_cost = pd.DataFrame({"route": routes, "cost": costs})
        return routes_cost.sort_values("cost", ascending=True)

    def next_generation(self, current_gen):
        # todo
        pass




