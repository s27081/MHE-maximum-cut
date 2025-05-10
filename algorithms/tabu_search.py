from algorithms.optimization_problem import max_cut_goal_function, random_partition, get_neighboorhood_solution


def tabu_search(graph, max_iterations, tabu_list_size):
    partition = random_partition(graph)
    best_partition = partition.copy()
    best_value = max_cut_goal_function(graph, best_partition, False)
    tabu_list = []
    steps_to_go_back = 15
    counter = 0

    for i in range(max_iterations):
        neighborhood = get_neighboorhood_solution(graph, partition, False)

        best_tabu = None
        best_tabu_value = 0
        best_move = 0

        for neighbor_partition, value in neighborhood:
            move = 0
            for p in range(len(partition)):
                if partition[p] != neighbor_partition[p]:
                    move = p
                    break

            if move in tabu_list:
                continue

            if value > best_tabu_value:
                best_tabu = neighbor_partition
                best_tabu_value = value
                best_move = move

        if best_tabu is None:
            break

        partition = best_tabu
        tabu_list.append(best_move)

        if len(tabu_list) > tabu_list_size:
            tabu_list.pop(0)

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
    print("Lista tabu: ", tabu_list)

    return best_value, best_partition
