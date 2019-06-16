from algorithms.dijkstra import Dijkstra
from algorithms.shortest import Shortest
from algorithms.random_path import Random
from algorithms.genetic import Genetic

AVAILABLE_ALGORITHMS = ["random", "shortest", "dijkstra"]
# AVAILABLE_ALGORITHMS = ["genetic"]
NUMBER_SIMULATED_PATHS = 10

algorithm_class = {
    "random": Random,
    "shortest": Shortest,
    "dijkstra": Dijkstra,
    "genetic": Genetic
}
