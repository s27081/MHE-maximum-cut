from algorithms.optimization_problem import max_cut_goal_function, random_partition, get_neighboorhood_solution
import random


# Funkcja wspinaczkowa z wyborem najlepszego sąsiada
def hill_climb_best_neighbour(graph, output):

    partition = random_partition(graph)
    initial_partition = partition
    solution = max_cut_goal_function(graph, partition, False)
    initial_solution = solution

    while True:
        neighbours = get_neighboorhood_solution(graph, partition, False)
        best_neighbour = 0
        best_cut = solution
        best_partition = partition
        for neighbour_partition, cut in neighbours:
            if cut > best_cut:
                if output:
                    print("Znaleziono lepsze rozwiązanie: ", neighbour_partition)
                    print("Podział sąsiada: ", cut)
                best_cut = cut
                best_partition = neighbour_partition

            if best_cut <= solution:
                break

            solution = best_cut

        print("=============")
        print("Rozwiązanie początkowe: ", initial_partition)
        print("Początkowy podział: ", initial_solution)
        print("Najlepszy sąsiad: ", best_partition)
        print("Końcowy podział: ", best_cut)

        return best_cut


# Funkcja wspinaczkowa z wyborem najlepszego sąsiada
def hill_climb_best_neighbour_random(graph, output):

    partition = random_partition(graph)
    initial_partition = partition.copy()
    solution = max_cut_goal_function(graph, partition, False)
    initial_solution = solution
    best_cut = solution
    best_partition = partition.copy()

    while True:
        neighbours = get_neighboorhood_solution(graph, partition, False)

        improving_neighbours = []
        for p, cut in neighbours:
            if cut > solution:
                improving_neighbours.append((p, cut))

        if not improving_neighbours:
            break

        best_partition, best_cut = random.choice(improving_neighbours)

        partition = best_partition
        solution = best_cut

        if output:
            print("Znaleziono lepsze rozwiązanie: ", best_partition)
            print("Podział sąsiada: ", best_cut)

    print("=============")
    print("Rozwiązanie początkowe: ", initial_partition)
    print("Początkowy podział: ", initial_solution)
    print("Najlepszy sąsiad: ", best_partition)
    print("Końcowy podział: ", best_cut)

    return best_cut
