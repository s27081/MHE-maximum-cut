import random
from algorithms.optimization_problem import max_cut_goal_function, random_partition


def genetic_main_island(graph, generations, population_size, crossover_method, mutation_rate, mutation_method,
                        num_islands, migration_rate, migration_interval):
    islands = []
    elite_size = 1
    for _ in range(num_islands):
        population = generate_population(graph, population_size)
        population.sort(key=lambda x: x[1], reverse=True)
        islands.append({
            "population": population,
            "best_cut": population[0][1],
            "best_gen": 0
        })

    for generation in range(generations):
        for idx, island in enumerate(islands):
            population = island["population"]
            new_population = []

            while len(new_population) < population_size:
                parent1 = tournament_selection(population)
                parent2 = tournament_selection(population)

                if crossover_method == "one_point":
                    child1, child2 = one_point_crossover(parent1, parent2, False)
                elif crossover_method == "uniform":
                    child1, child2 = uniform_crossover(parent1, parent2, False)
                else:
                    raise ValueError("Nieznana metoda krzyżowania")

                if mutation_method == "bit_flip_mutation":
                    child1 = bit_flip_mutation(child1, mutation_rate)
                    child2 = bit_flip_mutation(child2, mutation_rate)
                elif mutation_method == "swap_mutation":
                    child1 = swap_mutation(child1, mutation_rate)
                    child2 = swap_mutation(child2, mutation_rate)
                else:
                    raise ValueError("Nieznana metoda mutacji")

                new_population.append((child1, max_cut_goal_function(graph, child1, False)))
                new_population.append((child2, max_cut_goal_function(graph, child2, False)))

            new_population.sort(key=lambda x: x[1], reverse=True)
            island["population"] = new_population[:population_size - elite_size] + population[:elite_size]
            island["population"].sort(key=lambda x: x[1], reverse=True)

            best = island["population"][0][1]
            print("Wyspa: ", (idx+1), " Generacja: ", (generation + 1), " Najlepszy wynik: ", best)

            if best > island["best_cut"]:
                island["best_cut"] = best
                island["best_gen"] = generation + 1

        if migration_interval > 0 and (generation + 1) % migration_interval == 0:
            for i in range(num_islands):
                src = islands[i]
                dst = islands[(i + 1) % num_islands]

                migrants = random.sample(src["population"], migration_rate)
                individual_to_replace_list = list(range(len(dst["population"])))
                random.shuffle(individual_to_replace_list)
                for j in range(migration_rate):
                    dst["population"][individual_to_replace_list[j]] = migrants[j]

    for i, island in enumerate(islands):
        print("Wyspa: ", i+1, " Najlepsza generacja: ", island['best_gen'], " Najlepsze cięcie: ", island['best_cut'])


def tournament_selection(population):
    k = len(population) // 2
    picked_individual = random.sample(population, k)
    best_individual = picked_individual[0]
    for individual in picked_individual[1:]:
        if individual[1] > best_individual[1]:
            best_individual = individual
    return best_individual


def generate_population(graph, population_size):
    population = []
    for _ in range(population_size):
        individual_partition = random_partition(graph)
        fitness_cut = max_cut_goal_function(graph, individual_partition, False)
        population.append((individual_partition, fitness_cut))
    return population


def one_point_crossover(parent1, parent2, output):
    parent1_dict = parent1[0]
    parent2_dict = parent2[0]
    point = random.randint(1, len(parent1_dict)-2)
    keys = list(parent1_dict.keys())

    child1 = {}
    child2 = {}

    for i in range(len(keys)):
        key = keys[i]
        if i < point:
            child1[key] = parent1_dict[key]
            child2[key] = parent2_dict[key]
        else:
            child1[key] = parent2_dict[key]
            child2[key] = parent1_dict[key]
    if output:
        print("Powstałe dzieci (one_point): ", child1, " ", child2)
    return child1, child2


def uniform_crossover(parent1, parent2, output):
    parent1_dict = parent1[0]
    parent2_dict = parent2[0]
    keys = list(parent1_dict.keys())

    child1 = {}
    child2 = {}

    for i in range(len(keys)):
        key = keys[i]
        if random.randint(0, 1) == 0:
            child1[key] = parent1_dict[key]
            child2[key] = parent2_dict[key]
        else:
            child1[key] = parent2_dict[key]
            child2[key] = parent1_dict[key]
    if output:
        print("Powstałe dzieci (uniform): ", child1, " ", child2)
    return child1, child2


def bit_flip_mutation(partition, mutation_rate):
    mutation = partition.copy()
    for node in mutation:
        if random.random() < mutation_rate:
            mutation[node] = 1 - mutation[node]
    return mutation


def swap_mutation(partition, mutation_rate):
    mutation = partition.copy()
    if random.random() < mutation_rate:
        keys = list(mutation.keys())
        p1, p2 = random.sample(keys, 2)
        mutation[p1], mutation[p2] = mutation[p2], mutation[p1]
    return mutation
