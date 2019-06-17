from collections import deque, namedtuple

from .base import BaseAlgorithm

inf = float('inf')
Edge = namedtuple('Edge', 'start, end, cost')


def make_edge(start, end, cost=1):
    return Edge(start, end, cost)


class Dijkstra(BaseAlgorithm):
    def __init__(self, map, ncars_by_street):
        super().__init__(map, ncars_by_street)
        self.edges = self.get_edges()

    def get_edges(self):
        edges = []
        for street1, adjacent_streets in self.map.graph.items():
            if street1 in self.ncars_by_street.columns.values.tolist():
                cars_on_street1 = sum(self.ncars_by_street[street1])
            else:
                cars_on_street1 = 0
            for street2 in adjacent_streets:
                edge = (street1, street2, cars_on_street1)
                edges.append(edge)
        return [make_edge(*edge) for edge in edges]

    @property
    def vertices(self):
        return set(sum(([edge.start, edge.end] for edge in self.edges), []))

    @property
    def neighbours(self):
        neighbours = {vertex: set() for vertex in self.vertices}
        for edge in self.edges:
            neighbours[edge.start].add((edge.end, edge.cost))

        return neighbours

    def get_route(self, source, dest):
        assert source in self.vertices, 'Such source node doesn\'t exist'
        distances = {vertex: inf for vertex in self.vertices}
        previous_vertices = {
            vertex: None for vertex in self.vertices
        }
        distances[source] = 0
        vertices = self.vertices.copy()

        while vertices:
            current_vertex = min(
                vertices, key=lambda vertex: distances[vertex])
            vertices.remove(current_vertex)
            if distances[current_vertex] == inf:
                break
            for neighbour, cost in self.neighbours[current_vertex]:
                alternative_route = distances[current_vertex] + cost
                if alternative_route < distances[neighbour]:
                    distances[neighbour] = alternative_route
                    previous_vertices[neighbour] = current_vertex

        path, current_vertex = deque(), dest
        while previous_vertices[current_vertex] is not None:
            path.appendleft(current_vertex)
            current_vertex = previous_vertices[current_vertex]
        if path:
            path.appendleft(current_vertex)
        return list(path)

# graph = Dijkstra([('rua1', 'rua2', 2), ('rua2', 'rua4', 3), ('rua2', 'rua3', 3)])
# print(graph.dijkstra("rua1", "rua3"))
