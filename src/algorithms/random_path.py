from .base import BaseAlgorithm


class Random(BaseAlgorithm):
    def __init__(self, map, ncars_by_street):
        super().__init__(map, ncars_by_street)

    def get_route(self, source, dest, path=[]):
        path = path + [source]
        if source == dest:
            return path
        if source not in self.map.graph:
            return None
        for node in self.map.graph[source]:
            if node not in path:
                new_path = self.get_route(node, dest, path)
                if new_path:
                    return new_path
        return None
