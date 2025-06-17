import random
from algorithms.optimization_problem import max_cut_goal_function, random_partition


def genetic_main(graph, generations, population_size, crossover_method, mutation_rate, mutation_method, stop_condition, max_no_improving_generations):
    population = generate_population(graph, population_size)
    population.sort(key=lambda x: x[1], reverse=True)
    no_improving_generations = 0
    best_generation = 0
    best_cut = max_cut_goal_function(graph, population[0][0], False)
    elite_size = 1

    for generation in range(generations):
        new_population = []

        while len(new_population) < population_size:
            parent1 = tournament_selection(population)
            parent2 = tournament_selection(population)
            if crossover_method == "one_point":
                child1, child2 = one_point_crossover(parent1, parent2, False)
            elif crossover_method == "uniform":
                child1, child2 = uniform_crossover(parent1, parent2, False)
            else:
                raise ValueError("Brak takiego łączenia generacji")

            if mutation_method == "bit_flip_mutation":
                child1 = bit_flip_mutation(child1, mutation_rate)
                child2 = bit_flip_mutation(child2, mutation_rate)
            elif mutation_method == "swap_mutation":
                child1 = swap_mutation(child1, mutation_rate)
                child2 = swap_mutation(child2, mutation_rate)
            else:
                raise ValueError("Brak mutacji")

            fitness_cut_child1 = max_cut_goal_function(graph, child1, False)
            fitness_cut_child2 = max_cut_goal_function(graph, child2, False)

            new_population.append((child1, fitness_cut_child1))
            new_population.append((child2, fitness_cut_child2))

        new_population.sort(key=lambda x: x[1], reverse=True)
        # population = new_population_sorted[:population_size]
        population = new_population[:population_size - elite_size] + population[:elite_size]

        population.sort(key=lambda x: x[1], reverse=True)

        print("Generacja: ", generation+1, " najlepszy wynik: ", population[0][1])

        if population[0][1] > best_cut:
            best_cut = population[0][1]
            best_generation = generation + 1
            no_improving_generations = 0
        else:
            no_improving_generations += 1

        if stop_condition == 'max_generations' and generation + 1 >= generations:
            print("Koniec. Maksymalna ilość generacji: ", generation)
            break
        elif stop_condition == "no_improvement" and no_improving_generations >= max_no_improving_generations:
            print("Koniec. Maksymalna ilość iteracji bez poprawy: ", no_improving_generations)
            break

    print("======================")
    print("Najlepsza generacja: ", best_generation)
    print("Najlepsze cięcie: ", best_cut)


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
