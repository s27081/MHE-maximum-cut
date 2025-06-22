import argparse
import tools.graph_tools as graph_tools
import algorithms.optimization_problem as optimization
import algorithms.full_search as full
import algorithms.hill_climb as hill
import algorithms.tabu_search as tabu
import algorithms.simulate_annealing as annealing
import algorithms.genetic_main as gen_main
import algorithms.genetic_main_parallel as gen_main_par
import algorithms.genetic_main_island as gen_main_is
import tools.experiment as exp
import time


def check_time(func, *args, **kwargs):
    start_time = time.time()
    func(*args, **kwargs)
    end_time = time.time()
    print("Czas wykonywania: ", (end_time - start_time), " sekund")


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
    parser.add_argument("-gm", "--genetic_main", action="store_true", help="Funkcja genetyczna")
    parser.add_argument("-gmg", "--genetic_main_generations", type=int, default=50, help="Generacje")
    parser.add_argument("-gmp", "--genetic_main_population_size", type=int, default=20, help="Populacja")
    parser.add_argument("-gmc", "--genetic_main_crossover", type=str, choices=["one_point", "uniform"],  default="one_point", help="Łączenie generacji")
    parser.add_argument("-gmm", "--genetic_main_mutation_rate", type=float, default=0.1, help="Współczynnik mutacji")
    parser.add_argument("-gmt", "--genetic_main_mutation_method", type=str, choices=["bit_flip_mutation", "swap_mutation"], default="bit_flip_mutation", help="Rodzaj mutacji")
    parser.add_argument("-gms", "--genetic_main_stop_condition", type=str, choices=["max_generations", "no_improvement"], default="no_improvement", help="Warunek zakończenia")
    parser.add_argument("-gmi", "--genetic_main_max_no_improving_generations", type=int, default=10, help="Limit generacji bez poprawy")
    parser.add_argument("-gp", "--genetic_main_parallel", action="store_true", help="Funkcja genetyczna równoległa")
    parser.add_argument("-gi", "--genetic_main_island", action="store_true", help="Funkcja genetyczna wyspy")
    parser.add_argument("-gin", "--genetic_main_island_number", type=int, default=3, help="Liczba wysp dla algorytmu genetycznego")
    parser.add_argument("-gimr", "--genetic_main_island_migration_rate", type=int, default=3 , help="Liczba osobników migrujących dla algorytmu genetycznego")
    parser.add_argument("-gimi", "--genetic_main_island_migration_interval", type=int, default=3, help="Co ile generacji osobniki migrują")
    parser.add_argument("-tc", "--time_checker", action="store_true", help="Sprawdź czas wykonywania programu")
    parser.add_argument("-e", "--experiment", action="store_true", help="Porównaj dwie metody")

    args = parser.parse_args()
    graph, vertices, edges = graph_tools.load_graph(args.graph)

    def run(func, *f_args, **f_kwargs):
        if args.time_checker:
            check_time(func, *f_args, **f_kwargs)
        else:
            func(*f_args, **f_kwargs)

    if args.random_partition:
        run(optimization.random_partition, graph)

    elif args.max_cut:
        partition = optimization.random_partition(graph)
        run(optimization.max_cut_goal_function, graph, partition, False)

    elif args.neighborhood:
        partition = optimization.random_partition(graph)
        run(optimization.get_neighboorhood_solution, graph, partition, False)

    elif args.full_search:
        run(full.full_search, graph, vertices)

    elif args.hill_climb_classic:
        run(hill.hill_climb_best_neighbour, graph, False)

    elif args.hill_climb_random:
        run(hill.hill_climb_best_neighbour_random, graph, False)

    elif args.tabu_search:
        run(tabu.tabu_search,
            graph,
            max_iterations=args.tabu_iterations,
            tabu_list_size=args.tabu_list_size,
            tabu_history_size=args.tabu_history_size,
            output=True)

    elif args.simulate_annealing:
        run(annealing.simulate_annealing,
            graph,
            temperature=args.simulate_annealing_temperature,
            max_iter=args.simulate_annealing_max_iteration,
            cooling_rate=args.simulate_annealing_cooling_rate,
            output=True)

    elif args.genetic_main:
        run(gen_main.genetic_main,
            graph,
            generations=args.genetic_main_generations,
            population_size=args.genetic_main_population_size,
            crossover_method=args.genetic_main_crossover,
            mutation_rate=args.genetic_main_mutation_rate,
            mutation_method=args.genetic_main_mutation_method,
            stop_condition=args.genetic_main_stop_condition,
            max_no_improving_generations=args.genetic_main_max_no_improving_generations,
            output=True)
    elif args.genetic_main_parallel:
        run(gen_main_par.genetic_main_parallel,
            graph,
            generations=args.genetic_main_generations,
            population_size=args.genetic_main_population_size,
            crossover_method=args.genetic_main_crossover,
            mutation_rate=args.genetic_main_mutation_rate,
            mutation_method=args.genetic_main_mutation_method,
            stop_condition=args.genetic_main_stop_condition,
            max_no_improving_generations=args.genetic_main_max_no_improving_generations)
    elif args.genetic_main_island:
        run(gen_main_is.genetic_main_island,
            graph,
            generations=args.genetic_main_generations,
            population_size=args.genetic_main_population_size,
            crossover_method=args.genetic_main_crossover,
            mutation_rate=args.genetic_main_mutation_rate,
            mutation_method=args.genetic_main_mutation_method,
            num_islands=args.genetic_main_island_number,
            migration_rate=args.genetic_main_island_migration_rate,
            migration_interval=args.genetic_main_island_migration_interval,
            output=True)
    elif args.experiment:
        run(exp.experiment, graph)

if __name__ == "__main__":
    main()
