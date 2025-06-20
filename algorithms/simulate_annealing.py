from algorithms.optimization_problem import max_cut_goal_function, random_partition, get_neighboorhood_solution
import random
import math


def simulate_annealing(graph, temperature, cooling_rate, max_iter, output=True):
    partition = random_partition(graph)
    cut = max_cut_goal_function(graph, partition, False)
    best_partition = partition.copy()
    best_cut = cut
    temp = temperature
    score_history = [cut]

    for i in range(max_iter):
        neighborhood = get_neighboorhood_solution(graph, partition, False)

        neighbor_partition, neighbor_cut = random.choice(neighborhood)

        delta = neighbor_cut - cut

        if delta > 0 or math.exp(delta / temp) > random.random():
            partition = neighbor_partition
            cut = neighbor_cut

            if neighbor_cut > best_cut:
                best_partition = neighbor_partition
                best_cut = neighbor_cut

        temp *= cooling_rate
        score_history.append(best_cut)
        if output:
            print("Podział: ", cut, " Najlepszy podział: ", best_cut, " Temperatura: ", temp)

    return best_cut, score_history
