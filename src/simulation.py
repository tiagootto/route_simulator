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


def get_map():
    g = Graph()
    g.add_edge("rua1", "rua2")
    g.add_edge("rua2", "rua5")
    g.add_edge("rua2", "rua4")
    g.add_edge("rua4", "rua5")
    g.add_edge("rua4", "rua3")
    g.add_edge("rua5", "rua3")
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


def main(algorithms, n_simulated_paths):
    map = get_map()
    random_cars = get_random_paths(map, n_simulated_paths)

    ncars_by_route = get_ncars_by_route(random_cars)
    # print(map)
    print(map.graph)
    # print(ncars_by_route)

    for algo_name in algorithms:
        logging.info("Computing {}...".format(algo_name))
        algo = config.algorithm_class[algo_name](map, ncars_by_route)
        algo_route = algo.get_route("rua1", "rua3")
        logging.info("Route: {}".format(algo_route))
        logging.info("Time taken to complete the route: {}".format(get_total_route_time(algo_route, ncars_by_route)))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("algorithm", nargs='?', default=config.AVAILABLE_ALGORITHMS,
                        help="Algorithm that you want to try it")
    parser.add_argument("simulated_paths",  nargs='?', type=int, default=config.NUMBER_SIMULATED_PATHS,
                        help="Number of simulated paths")
    args = parser.parse_args()

    if args.algorithm == 'all' or args.algorithm == config.AVAILABLE_ALGORITHMS:
        algorithm_to_simulate = config.AVAILABLE_ALGORITHMS
    elif args.algorithm not in config.AVAILABLE_ALGORITHMS:
        msg_error = "Algorithm {} is not available".format(args.algorithm)
        raise NotImplementedError(msg_error)
    else:
        algorithm_to_simulate = [args.algorithm]
    simulated_paths = args.simulated_paths if args.simulated_paths else config.NUMBER_SIMULATED_PATHS

    main(algorithm_to_simulate, simulated_paths)
