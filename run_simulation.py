import argparse
import logging
import random
import itertools
import sys
import pandas as pd
import numpy as np

from routes.graph import Graph
from utils import get_total_route_time
import config

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def get_map(draw=False):
    g = Graph()
    for node1, node2 in config.map_connections:
        g.add_edge(node1, node2)
    if draw:
        g.draw_graph()
    return g


def get_random_paths(routes, number_of_cars):
    paths = []
    for i in range(number_of_cars):
        source = random.choice(routes.get_nodes_with_childrens())
        dest = random.choice(routes.get_all_edges_from_node(source))
        path = routes.find_path(source, dest)
        paths.append(path)
    return paths


def get_ncars_by_route(car_paths):
    """
    [['rua1', 'rua2', 'rua3'], ['rua1', 'rua2']] ->
       rua1  rua3  rua2
    0     2     0     0
    1     0     0     2
    2     0     1     0
    :param car_paths:
    :return:
    """
    length_max_path = len(max(car_paths, key=len))
    routes = list(set(itertools.chain(*car_paths)))
    res = pd.DataFrame(0, index=np.arange(length_max_path), columns=routes)

    for path in car_paths:
        for i in range(len(path)):
            res.loc[i, path[i]] += 1

    return res


def main(algorithms, n_simulations):
    map = get_map()

    res = pd.DataFrame(columns=algorithms)
    for i in range(n_simulations):
        random_cars = get_random_paths(map, config.NUMBER_NORMAL_CARS)
        ncars_by_route = get_ncars_by_route(random_cars)
        i_res = []
        for algo_name in algorithms:
            logging.info("Computing {}...".format(algo_name))
            algo = config.algorithm_class[algo_name](map, ncars_by_route)
            algo_route = algo.get_route("source", "dest")
            total_route_time = get_total_route_time(algo_route, ncars_by_route)
            logging.info("Route: {}".format(algo_route))
            logging.info("Time taken to complete the route: {}".format(total_route_time))

            i_res.append(total_route_time)
        res = res.append(pd.Series(i_res, index=algorithms), ignore_index=True)
    print(res.apply(pd.to_numeric).describe())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("algorithm", nargs='?', default=config.AVAILABLE_ALGORITHMS,
                        help="Algorithm that you want to try it")
    parser.add_argument("number_simulations",  nargs='?', type=int, default=config.NUMBER_SIMULATIONS,
                        help="Number of simulated paths")
    args = parser.parse_args()

    if args.algorithm == 'all' or args.algorithm == config.AVAILABLE_ALGORITHMS:
        algorithm_to_simulate = config.AVAILABLE_ALGORITHMS
    elif args.algorithm not in config.AVAILABLE_ALGORITHMS:
        msg_error = "Algorithm {} is not available".format(args.algorithm)
        raise NotImplementedError(msg_error)
    else:
        algorithm_to_simulate = [args.algorithm]

    n_simulations = args.number_simulations if args.number_simulations else config.NUMBER_SIMULATIONS

    main(algorithm_to_simulate, n_simulations)
