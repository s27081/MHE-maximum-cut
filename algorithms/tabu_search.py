from algorithms.optimization_problem import max_cut_goal_function, random_partition, get_neighboorhood_solution


def tabu_search(graph, max_iterations):
    partition = random_partition(graph)
    best_partition = partition.copy()
    best_value = max_cut_goal_function(graph, partition, False)
    tabu_list = []
    steps_to_go_back = 3

    for i in range(max_iterations):
        best_tabu = None
        best_tabu_value = 0
        best_move = None
        counter = 0

        for v in range(len(graph)):
            if v in tabu_list:
                continue

            tabu_next = partition.copy()
            tabu_next[v] = 1 - tabu_next[v]
            value = max_cut_goal_function(graph, tabu_next, False)

            if value > best_tabu_value:
                best_tabu = tabu_next
                best_tabu_value = value
                best_move = v

        if best_tabu is None:
            break

        partition = best_tabu
        tabu_list.append(best_move)

        if best_tabu_value > best_value:
            best_partition = best_tabu
            best_value = best_tabu_value
            counter = 0
            print("Znaleziono nową wartość: ", best_value)
            print("Znaleziono nową partyjcę: ", best_partition)
        else:
            counter += 1

        if counter >= steps_to_go_back:
            print("Cofnięcie do ostatniego najlepszego rozwiązania: ", best_partition)
            partition = best_partition.copy()
            counter = 0

    print("Największy podział: ", best_value)
    print("Najlepszy podział: ", best_partition)

    return best_value, best_partition

