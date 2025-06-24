#dijkstra_path            (G, DiG)
#       -Restituisce il cammino più breve (come lista di nodi) dal nodo source al nodo target nel grafo G, usando l’algoritmo di Dijkstra
#       -richiede entrambi i nodi (source e target).
#              -Se conosci solo il nodo di partenza e vuoi i percorsi verso tutti, usa invece nx.single_source_dijkstra_path
#       -es --> pathDijkstra = nx.dijkstra_path(self._grafo, u, v, weight=None)
import networkx as nx

#nx.shortest_path        (G, DiG)
#       -Calcola il cammino più breve (come lista di nodi) tra due nodi source e target
#           -Dijkstra se specifichi weight
#           -BFS se weight=None (cioè grafi non pesati)

#longest path

#nx.bfs_predecessors(G, source)   (G, DiG)
#       -Restituisce un dizionario {nodo: predecessore} per tutti i nodi visitati in una BFS (breadth-first search) a partire da source
#       -myDict = dict(nx.bfs_predecessors(G, u))

