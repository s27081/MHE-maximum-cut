# Ładowanie grafu z pliku filename, zwracamy graf, jego wieszchołki i krawędzie
def load_graph(filename):
    graph = {}
    edges = set()
    with open(filename, "r") as file:
        for line in file:
            node1, node2, weight = map(int, line.split())
            if node1 not in graph:
                graph[node1] = []
            if node2 not in graph:
                graph[node2] = []

            graph[node1].append((node2, weight))
            graph[node2].append((node1, weight))

            edges.add((node1, node2, weight))
        print("Graf: \n", dict(sorted(graph.items())))
        print("Liczba wieszchołków: ", len(graph))
        print("Liczba krawędzi: ", len(edges))
    return dict(sorted(graph.items())), len(graph), len(edges)
