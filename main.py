import argparse
import tools.graph_tools as graph_tools
import algorithms.optimization_problem as optimization
import algorithms.full_search as full
import algorithms.hill_climb as hill
import algorithms.tabu_search as tabu

def main():
    parser = argparse.ArgumentParser(description="Maximum cut problem")

    parser.add_argument("-r", "--random_partition", action="store_true", help="Losowy podział grafu na dwa podzbiory")
    parser.add_argument("-m", "--max_cut", action="store_true", help="Funkcja celu dla maximum cut")
    parser.add_argument("-n", "--neighborhood", action="store_true", help="Funkcja sprawdzająca sąsiedztwo")
    parser.add_argument("-f", "--full_search", action="store_true", help="Funkcja pełnego przeglądu")
    parser.add_argument("-w1", "--hill_climb_classic", action="store_true", help="Funkcja wspinaczkowa z wyborem najlepszego sąsiada")
    parser.add_argument("-w2", "--hill_climb_random", action="store_true", help="Funkcja wspinaczkowa z wyborem losowego sąsiada")
    parser.add_argument("-t", "--tabu_search", action="store_true", help="Funkcja tabu")

    args = parser.parse_args()
    graph, vertices, edges = graph_tools.load_graph("./tools/data.txt")

    if args.random_partition:
        optimization.random_partition(graph)

    elif args.max_cut:
        partition = optimization.random_partition(graph)
        optimization.max_cut_goal_function(graph, partition, True)

    elif args.neighborhood:
        partition = optimization.random_partition(graph)
        optimization.get_neighboorhood_solution(graph, partition)
        
    elif args.full_search:
        full.full_search(graph, vertices)

    elif args.hill_climb_classic:
        hill.hill_climb_best_neighbour(graph)

    elif args.hill_climb_random:
        hill.hill_climb_best_neighbour_random(graph)

    elif args.tabu_search:
        tabu.tabu_search(graph, 1200)



if __name__ == "__main__":
    main()
