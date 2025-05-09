from algorithms.optimization_problem import max_cut_goal_function


# Generowanie wszystkich podziałów
def generate_all_partitions(vertices):
    number_of_partitions = 2 ** vertices
    partitions = []
    for i in range(number_of_partitions):
        partition = []
        for j in range(vertices):
            if (i >> j) & 1:
                partition.append(1)
            else:
                partition.append(0)
        partitions.append(partition)
    return partitions


# Funkcja pełnego przeglądu
def full_search(graph, vertices):
    max_cut = 0
    best_partition = 0
    all_partitions = generate_all_partitions(vertices)

    for p in all_partitions:
        cut_value = max_cut_goal_function(graph, p, False)
        if cut_value > max_cut:
            max_cut = cut_value
            best_partition = p

    print("Najlepszy podział: ", max_cut)
    print("Najlepsza partycja: ", best_partition)

    return max_cut, best_partition
