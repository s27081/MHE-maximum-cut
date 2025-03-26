import random
from tools import graph_tools

graph, vertices, edges = graph_tools.load_graph("../data.txt")

# Losowy podział grafu na dwa podzbiory
def random_partition(graph):
    partition = {}
    for node in graph:
        partition[node] = random.choice([0,1])
    print("Losowy podział: ",partition)
    return partition

# Funkcja celu dla maximum cut
def max_cut_goal_function(graph, partition):
    total_cut = 0

    for node1 in graph:
        for node2, weight in graph[node1]:
            if node1 < node2:
                if partition[node1] != partition[node2]:
                    total_cut += weight
    print("Całowity podział: ", total_cut)
    return total_cut

# Funkcja sprawdzająca sąsiedztwo bieżącego rozwiązania
def get_neighboorhood_solution(graph, partition):

    neighborhood = []

    for node in graph:
        neighbor_partition = partition.copy()
        neighbor_partition[node] = 1 - neighbor_partition[node]

        print("=================")
        print("Sąsiad: ", node)
        neighbor_total_cut = max_cut_goal_function(graph, neighbor_partition)

        neighborhood.append((neighbor_partition, neighbor_total_cut))

    return neighborhood

