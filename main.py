import argparse
import tools.graph_tools as graph_tools
import algorithms.optimization_problem as optimization
import algorithms.full_search as full
import algorithms.hill_climb as hill
import algorithms.tabu_search as tabu
import algorithms.simulate_annealing as annealing

def main():
    parser = argparse.ArgumentParser(description="Maximum cut problem")

    parser.add_argument("-r", "--random_partition", action="store_true", help="Losowy podział grafu na dwa podzbiory")
    parser.add_argument("-m", "--max_cut", action="store_true", help="Funkcja celu dla maximum cut")
    parser.add_argument("-n", "--neighborhood", action="store_true", help="Funkcja sprawdzająca sąsiedztwo")
    parser.add_argument("-f", "--full_search", action="store_true", help="Funkcja pełnego przeglądu")
    parser.add_argument("-w1", "--hill_climb_classic", action="store_true", help="Funkcja wspinaczkowa z wyborem najlepszego sąsiada")
    parser.add_argument("-w2", "--hill_climb_random", action="store_true", help="Funkcja wspinaczkowa z wyborem losowego sąsiada")
    parser.add_argument("-t", "--tabu_search", action="store_true", help="Funkcja tabu")
    parser.add_argument("-g", "--graph", required=True, help="Ścieżka do pliku z grafem")
    parser.add_argument("-ti", "--tabu_iterations", type=int, default=80, help="Liczba iteracji dla tabu")
    parser.add_argument("-tl", "--tabu_list_size", type=int, default=8, help="Rozmiar listy tabu")
    parser.add_argument("-th", "--tabu_history_size", type=int, default=10, help="Rozmiar historii tabu")
    parser.add_argument("-s", "--simulate_annealing", action="store_true", help="Funkcja symulacji wyżarzania")
    parser.add_argument("-st", "--simulate_annealing_temperature", type=int, default=1000, help="Tempeatura wyżarzania")
    parser.add_argument("-si", "--simulate_annealing_max_iteration", type=int, default=1000, help="Iteracje wyżarzania")
    parser.add_argument("-sr", "--simulate_annealing_cooling_rate", type=float, default=0.95, help="Ratio wychładzania")

    args = parser.parse_args()
    graph, vertices, edges = graph_tools.load_graph(args.graph)

    if args.random_partition:
        optimization.random_partition(graph)

    elif args.max_cut:
        partition = optimization.random_partition(graph)
        optimization.max_cut_goal_function(graph, partition, True)

    elif args.neighborhood:
        partition = optimization.random_partition(graph)
        optimization.get_neighboorhood_solution(graph, partition, True)
        
    elif args.full_search:
        full.full_search(graph, vertices)

    elif args.hill_climb_classic:
        hill.hill_climb_best_neighbour(graph)

    elif args.hill_climb_random:
        hill.hill_climb_best_neighbour_random(graph)

    elif args.tabu_search:
        tabu.tabu_search(graph,
                max_iterations=args.tabu_iterations,
                tabu_list_size=args.tabu_list_size,
                tabu_history_size=args.tabu_history_size)

    elif args.simulate_annealing:
        annealing.simulate_annealing(graph,
                temperature=args.simulate_annealing_temperature,
                max_iter=args.simulate_annealing_max_iteration,
                cooling_rate=args.simulate_annealing_cooling_rate)



if __name__ == "__main__":
    main()
