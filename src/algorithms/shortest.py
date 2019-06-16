from .base import BaseAlgorithm


class Shortest(BaseAlgorithm):
    def __init__(self, map, ncars_by_street):
        super().__init__(map, ncars_by_street)

    def get_route(self, source, dest, path=[]):
        path = path + [source]
        if source == dest:
            return path
        shortest = None
        for node in self.map.graph[source]:
            if node not in path:
                newpath = self.get_route(node, dest, path)
                if newpath:
                    if not shortest or len(newpath) < len(shortest):
                        shortest = newpath
        return shortest
