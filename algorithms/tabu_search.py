from algorithms.optimization_problem import max_cut_goal_function, random_partition, get_neighboorhood_solution


def tabu_search(graph, max_iterations, tabu_list_size, tabu_history_size, output=True):
    partition = random_partition(graph)
    best_partition = partition.copy()
    cut = max_cut_goal_function(graph, best_partition, False)
    tabu_list = []
    tabu_history_list = []

    best_cut = cut
    score_history = [best_cut]

    for i in range(max_iterations):
        neighborhood = get_neighboorhood_solution(graph, partition, False)
        best_tabu = None
        best_tabu_cut = 0

        for neighbor, neighbor_cut in neighborhood:
            if neighbor not in tabu_list or neighbor_cut > best_cut:
                if neighbor_cut > best_tabu_cut:
                    best_tabu = neighbor
                    best_tabu_cut = neighbor_cut

        if best_tabu is None:
            history_workspace = return_to_working_point(graph, tabu_history_list, tabu_list, False)
            if history_workspace:
                partition = history_workspace[0]
                cut = best_tabu_cut
                if output:
                    print("Powrót do punktu roboczego:", history_workspace[0])
            else:
                if output:
                    print("Brak punktu powrotu")

        tabu_history_list.append((partition, best_cut))

        if best_tabu is not None:
            tabu_list.append(best_tabu)
            cut = best_tabu_cut
            partition = best_tabu

        if cut > best_cut:
            best_cut = cut
            best_partition = partition.copy()

        if len(tabu_history_list) > tabu_history_size:
            tabu_history_list.pop()

        if len(tabu_list) > tabu_list_size:
            tabu_list.pop()

        score_history.append(best_cut)
    if output:
        print("===================")
        print("Największy podział: ", best_cut)
        print("Najlepszy podział: ", best_partition)
        print("Lista tabu: ", tabu_list)

    return best_cut, score_history


def return_to_working_point(graph, tabu_history_list, tabu_list, output):
    for _ in tabu_history_list:
        working_point = tabu_history_list.pop()
        neighbours = get_neighboorhood_solution(graph, working_point[0], False)
        for neighbour in neighbours:
            if neighbour not in tabu_list:
                neigh_cut = max_cut_goal_function(graph, neighbour, False)
                if neigh_cut > working_point[1]:
                    if output:
                        print("Dostępny lepszy punkt roboczy", working_point[0])
                    return working_point
    if output:
        print("Brak lepszych punktów roboczych")
    return None
