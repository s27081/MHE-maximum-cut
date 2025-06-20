import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import psutil
import random

import algorithms.tabu_search as tabu
import algorithms.simulate_annealing as annealing
import algorithms.genetic_main as genetic


def run_method(method_func, graph, params, num_runs=5):
    all_scores = []
    all_times = []
    all_memories = []
    iteration_history = []
    for _ in range(num_runs):
        result, elapsed, memory = measure_performance(method_func, graph, **params)

        if isinstance(result, tuple):
            score = result[0]
            iteration_history = result[1]
        else:
            score = result

        all_scores.append(score)
        all_times.append(elapsed)
        all_memories.append(memory)

    avg_scores = np.mean(all_scores, axis=0)
    avg_time = np.mean(all_times)
    avg_memory = np.mean(all_memories)
    return avg_scores, avg_time, all_scores, all_times, avg_memory, iteration_history


def experiment(graph):
    results = evaluate_all_configs(graph, tabu, annealing, run_method)
    best_tabu_result, best_annealing_result, best_genetic_result = compare_best_results(results)

    # Top 5 runów
    plot_convergence_histories(best_tabu_result['score_history'], "Tabu Search - 5 runów dla najlepszych parametrów", "Tabu")
    plot_convergence_histories(best_annealing_result['score_history'], "Simulated - 5 runów dla najlepszych parametrów", "Annealing")
    plot_convergence_histories(best_genetic_result['score_history'], "Genetic - 5 runów dla najlepszych parametrów","Genetic")

    # Iteracje wewnątrz algorytmu
    plot_convergence_histories(best_tabu_result['iteration'], "Tabu Search Iteracje", "Tabu")
    plot_convergence_histories(best_annealing_result['iteration'], "Simulated Annealing Iteracje", "Annealing")
    plot_convergence_histories(best_genetic_result['iteration'], "Genetic Iteracje", "Genetic")

    # Porównanie
    compare_methods(best_tabu_result['iteration'], best_annealing_result['iteration'], best_genetic_result['iteration'])
    return results


def evaluate_all_configs(graph, tabu, annealing, run_method):

    results = {
        'tabu_search': [],
        'annealing': [],
        'genetic': []
    }

    tabu_params_list = random_tabu_params()
    annealing_params_list = random_annealing_params()
    genetic_params_list = random_genetic_params()

    # Tabu Search
    for params in tabu_params_list:
        score, elapsed, score_history, time_history, memory_usage, iteration_history = run_method(tabu.tabu_search, graph, params)
        results['tabu_search'].append({'params': params, 'score': score, 'time': elapsed, 'score_history': score_history, 'time_history': time_history, 'memory_usage' : memory_usage, 'iteration_history': iteration_history})

    # Simulated Annealing
    for params in annealing_params_list:
        score, elapsed, score_history, time_history, memory_usage, iteration_history = run_method(annealing.simulate_annealing, graph, params)
        results['annealing'].append({'params': params, 'score': score, 'time': elapsed, 'score_history': score_history, 'time_history': time_history, 'memory_usage' : memory_usage, 'iteration_history': iteration_history})

    # Genetic
    for params in genetic_params_list:
        score, elapsed, score_history, time_history, memory_usage, iteration_history = run_method(
            genetic.genetic_main, graph, params)
        results['genetic'].append({'params': params, 'score': score, 'time': elapsed, 'score_history': score_history,
                                     'time_history': time_history, 'memory_usage': memory_usage,
                                     'iteration_history': iteration_history})
    return results


def compare_methods(tabu_history, annealing_history, genetic_history):
    plt.figure(figsize=(10, 5))
    x_tabu = range(1, len(tabu_history) + 1)
    x_annealing = range(1, len(annealing_history) + 1)
    x_genetic = range(1, len(genetic_history) + 1)
    plt.plot(x_tabu, tabu_history, label='Tabu Search', linewidth=2)
    plt.plot(x_annealing, annealing_history, label='Simulated Annealing', linewidth=2)
    plt.plot(x_genetic, genetic_history, label='Genetic', linewidth=2)
    plt.xlabel('Iteracja')
    plt.ylabel('Score')
    plt.title('Wykres Konwergencji')
    plt.legend()
    plt.grid(True)
    plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    plt.tight_layout()
    plt.show()

def plot_convergence_histories(histories, title, method_label):
    plt.figure(figsize=(10, 5))
    x_histories = range(1, len(histories) + 1)
    plt.plot(x_histories, histories, label=f"{method_label}")
    plt.xlabel("Iteracja")
    plt.ylabel("Score")
    plt.title(title)
    plt.grid(True)
    plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    plt.tight_layout()
    plt.show()

def compare_best_results(results):
    best_tabu_score = -float('inf')
    best_tabu_params = None
    best_tabu_score_history = None
    best_tabu_time = None
    best_tabu_memory = None
    best_tabu_iteration_history = None
    best_tabu_score_difference = None
    for entry in results['tabu_search']:
        if entry['score'] > best_tabu_score:
            best_tabu_score = entry['score']
            best_tabu_params = entry['params']
            best_tabu_score_history = entry['score_history']
            best_tabu_time = entry['time']
            best_tabu_memory = entry['memory_usage']
            best_tabu_iteration_history = entry['iteration_history']
            best_tabu_score_difference = max(entry['score_history']) - min(entry['score_history'])

    best_annealing_score = -float('inf')
    best_annealing_params = None
    best_annealing_history = None
    best_annealing_time = None
    best_annealing_memory = None
    best_annealing_iteration_history = None
    best_annealing_score_difference = None
    for entry in results['annealing']:
        if entry['score'] > best_annealing_score:
            best_annealing_score = entry['score']
            best_annealing_params = entry['params']
            best_annealing_history = entry['score_history']
            best_annealing_time = entry['time']
            best_annealing_memory = entry['memory_usage']
            best_annealing_iteration_history = entry['iteration_history']
            best_annealing_score_difference = max(entry['score_history']) - min(entry['score_history'])

    best_genetic_score = -float('inf')
    best_genetic_params = None
    best_genetic_history = None
    best_genetic_time = None
    best_genetic_memory = None
    best_genetic_iteration_history = None
    best_genetic_score_difference = None
    for entry in results['genetic']:
        if entry['score'] > best_genetic_score:
            best_genetic_score = entry['score']
            best_genetic_params = entry['params']
            best_genetic_history = entry['score_history']
            best_genetic_time = entry['time']
            best_genetic_memory = entry['memory_usage']
            best_genetic_iteration_history = entry['iteration_history']
            best_genetic_score_difference = max(entry['score_history']) - min(entry['score_history'])

    print("===== Porównanie najlepszych wyników =====")
    print(f"Tabu Search - Najlepszy wynik: {best_tabu_score}")
    print(f"Parametry: {best_tabu_params}")
    print(f"Czas: {best_tabu_time:3f} sekund")
    print(f"Odchył min/max: {best_tabu_score_difference}")
    print(f"Zużycie pamięci: {best_tabu_memory:.3f} MB")
    print()
    print(f"Simulated Annealing - Najlepszy wynik: {best_annealing_score}")
    print(f"Parametry: {best_annealing_params}")
    print(f"Czas: {best_annealing_time:.3f} sekund")
    print(f"Odchył min/max: {best_annealing_score_difference}")
    print(f"Zużycie pamięci: {best_annealing_memory} MB")
    print()
    print(f"Genetic - Najlepszy wynik: {best_genetic_score}")
    print(f"Parametry: {best_genetic_params}")
    print(f"Czas: {best_genetic_time:.3f} sekund")
    print(f"Odchył min/max: {best_genetic_score_difference}")
    print(f"Zużycie pamięci: {best_genetic_memory} MB")

    best_tabu = {'score': best_tabu_score,'params': best_tabu_params,'score_history': best_tabu_score_history, 'iteration': best_tabu_iteration_history}
    best_annealing = {'score': best_annealing_score,'params': best_annealing_params,'score_history': best_annealing_history, 'iteration': best_annealing_iteration_history}
    best_genetic = {'score': best_genetic_score, 'params': best_genetic_params,
                     'score_history': best_genetic_history, 'iteration': best_genetic_iteration_history}

    return best_tabu, best_annealing, best_genetic

def random_tabu_params(n=15):
    params_list = []
    for _ in range(n):
        params = {
            'max_iterations': random.choice([50, 75, 100, 125, 150]),
            'tabu_list_size': random.randint(3, 15),
            'tabu_history_size': random.randint(3, 15),
            'output': False
        }
        params_list.append(params)
    return params_list

def random_annealing_params(n=15):
    params_list = []
    for _ in range(n):
        params = {
            'temperature': random.choice([500, 1000, 1500, 2000]),
            'max_iter': random.choice([50, 75, 100, 125, 150]),
            'cooling_rate': round(random.uniform(0.85, 0.99), 3),
            'output': False
        }
        params_list.append(params)
    return params_list

def random_genetic_params(n=15):
    params_list = []
    for _ in range(n):
        params = {
            'generations': random.choice([10, 30, 50, 100, 150]),
            'population_size': random.choice([20, 50, 100, 200, 500]),
            'crossover_method': random.choice(["one_point", "uniform"]),
            'mutation_rate': random.choice([0.1, 0.2, 0.3, 0.5]),
            'mutation_method': random.choice(["bit_flip_mutation", "swap_mutation"]),
            'stop_condition': random.choice(["max_generations", "no_improvement"]),
            'max_no_improving_generations': random.choice([10, 15, 20, 50]),
            'output': False
        }
        params_list.append(params)
    return params_list


def measure_performance(func, *args, **kwargs):
    process = psutil.Process()
    initial_memory = process.memory_info().rss / (1024 * 1024)
    start_time = time.time()

    result = func(*args, **kwargs)

    elapsed_time = time.time() - start_time
    final_memory = process.memory_info().rss / (1024 * 1024)
    memory_usage = max(0, final_memory - initial_memory)

    return result, elapsed_time, memory_usage
