# Maximum Cut (Max-Cut) 
Problem NP-trudny, który polega na podziale wierzchołków grafu na dwie grupy w taki sposób, aby liczba (lub suma wag) k

## Komendy do prezentacji
* tabu_search
* ```python main.py -g ./tools/data2.txt -t -ti 100 -tl 10 -th 10
* simulated_annealing
* ```python main.py -g ./tools/data2.txt -s -st 1200 -si 200 -sr 0.96
* genetic_algorithm
* ```python main.py -g ./tools/data2.txt -gm -gmg 100 -gmp 25 -gmc one_point -gmm 0.2 -gmt bit_flip_mutation -gms no_improvement -gmi 15
* genetic_algorithm_island
* ```python main.py -g ./tools/data2.txt -gi -gimr 5 -gimi 5
* experiment
* ```python main.py -g ./tools/data2.txt -e 
