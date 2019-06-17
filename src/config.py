from algorithms.dijkstra import Dijkstra
from algorithms.shortest import Shortest
from algorithms.random_path import Random
from algorithms.genetic import Genetic

AVAILABLE_ALGORITHMS = ["random", "shortest", "dijkstra", "genetic"]
NUMBER_SIMULATED_PATHS = 20

algorithm_class = {
    "random": Random,
    "shortest": Shortest,
    "dijkstra": Dijkstra,
    "genetic": Genetic
}

map_connections = [["source", "street1"], ["source", "street2"],
                   ["street1", "street4"], ["street1", "street10"],
                   ["street2", "street3"], ["street2", "street3"],
                   ["street3", "street4"], ["street3", "street18"],
                   ["street4", "street9"], ["street12", "street3"],
                   ["street5", "street7"], ["street5", "street20"],
                   ["street6", "street8"], ["street6", "street21"],
                   ["street7", "source"], ["street7", "street10"],
                   ["street8", "street4"], ["street8", "street21"],
                   ["street9", "street4"], ["street9", "street16"],
                   ["street10", "street12"], ["street10", "street17"],
                   ["street11", "street12"],
                   ["street12", "street1"], ["street12", "street10"],
                   ["street13", "street9"], ["street13", "street3"],
                   ["street14", "street7"], ["street14", "street2"],
                   ["street15", "street8"], ["street15", "street3"],
                   ["street16", "source"], ["street16", "dest"],
                   ["street17", "street4"], ["street17", "dest"],
                   ["street18", "street11"], ["street18", "street22"],
                   ["street19", "street12"], ["street19", "street2"],
                   ["street20", "source"], ["street20", "street25"],
                   ["street21", "street1"], ["street21", "street10"],
                   ["street22", "street1"], ["street22", "street24"],
                   ["street23", "street3"], ["street23", "street10"],
                   ["street24", "street7"], ["street24", "dest"],
                   ["street25", "street6"], ["street25", "dest"]]
