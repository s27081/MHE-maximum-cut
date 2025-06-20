import random


# Losowy podział grafu na dwa podzbiory
def random_partition(graph):
    partition = {}
    for node in graph:
        partition[node] = random.choice([0,1])
    #print("Losowy podział: ",partition)
    return partition


# Funkcja celu dla maximum cut
def max_cut_goal_function(graph, partition, output):
    total_cut = 0

    for node1 in graph:
        for node2, weight in graph[node1]:
            if node1 < node2:
                if partition[node1] != partition[node2]:
                    total_cut += weight
    if output:
        print("Całowity podział: ", total_cut)
    return total_cut


# Funkcja sprawdzająca sąsiedztwo bieżącego rozwiązania
def get_neighboorhood_solution(graph, partition, output):

    neighborhood = []

    for node in graph:
        neighbor_partition = partition.copy()
        neighbor_partition[node] = 1 - neighbor_partition[node]
        if output:
            print("=================")
            print("Sąsiad: ", node)
            neighbor_total_cut = max_cut_goal_function(graph, neighbor_partition, True)
        else:
            neighbor_total_cut = max_cut_goal_function(graph, neighbor_partition, False)
        neighborhood.append((neighbor_partition, neighbor_total_cut))
    if output:
        print("Sąsiedztwo: ", neighborhood)

    return neighborhood

