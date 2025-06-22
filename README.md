# Maximum Cut (Max-Cut) 
Problem NP-trudny, który polega na podziale wierzchołków grafu na dwie grupy w taki sposób, aby liczba (lub suma wag) k

## Komendy do prezentacji
* tabu_search
```python main.py -g ./tools/data2.txt --tabu_search --tabu_iterations 100 --tabu_list_size 10 --tabu_history_size 10```
* simulated_annealing
```python main.py -g ./tools/data2.txt --simulate_annealing --simulate_annealing_temperature 1200 --simulate_annealing_temperature 200 --simulate_annealing_cooling_rate 0.96```
* genetic_algorithm
```python main.py -g ./tools/data2.txt --genetic_main --genetic_main_generations 100 --genetic_main_population_size 25 --genetic_main_crossover one_point --genetic_main_mutation_rate 0.2 --genetic_main_mutation_method bit_flip_mutation --genetic_main_stop_condition no_improvement --genetic_main_max_no_improving_generations 15```
* genetic_algorithm_island
```python main.py -g ./tools/data2.txt --genetic_main_island --genetic_main_island_number 5 --genetic_main_island_migration_rate 5 --genetic_main_island_migration_interval 5```
* experiment
```python main.py -g ./tools/data2.txt --experiment```
