import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict


class Graph:
    def __init__(self):
        self.graph = defaultdict(set)

    def get_all_nodes(self):
        nodes = set()
        for k, v in self.graph.items():
            nodes.add(k)
            nodes.update(v)
        print(list(nodes))
        return list(nodes)

    def add_edge(self, node1, node2):
        self.graph[node1].add(node2)

    def get_nodes_with_childrens(self):
        return list(self.graph.keys())

    def get_all_edges_from_node(self, node):
        """
        graph = {'street1': {'street2'}, 'street2': {'street4', 'street5'}, 'street4': {'street3', 'street5'},
        node = "street2" ->
        ['street5', 'street4', 'street3']
        """
        def rec_edges_nodes(node, edge_nodes):
            if node not in self.graph:
                return node
            for no in self.graph[node]:
                if no not in edge_nodes:
                    edge_nodes.append(no)
                    new_edges_nodes = rec_edges_nodes(no, edge_nodes)
            return edge_nodes
        return list(set(rec_edges_nodes(node, [])) - set(node))

    def print_graph(self):
        print(self.graph)

    def find_path(self, node1, node2, path=[]):
        """ Find any path between node1 and node2 (may not be shortest) """

        path = path + [node1]
        if node1 == node2:
            return path
        if node1 not in self.graph:
            return None
        for node in self.graph[node1]:
            if node not in path:
                new_path = self.find_path(node, node2, path)
                if new_path:
                    return new_path
        return None

    def find_all_possible_paths(self, node1, node):
        def deepth_first_search(graph, start, end, path, paths):
            path = path + [start]
            if start == end:
                paths.append(path)
            if start not in graph:
                return None
            for node in graph[start]:
                if node not in path:
                    deepth_first_search(graph, node, end, path, paths)
            return paths
        return deepth_first_search(self.graph, node1, node, [], [])

    def draw_graph(self):
        G = nx.DiGraph()
        for node1, v in self.graph.items():
            for node2 in v:
                G.add_edge(node1, node2)
        pos = nx.spring_layout(G)
        nx.draw(G, pos)
        plt.show()
