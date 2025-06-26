#LINK: https://networkx.org/documentation/stable/reference/algorithms/traversal.html

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


#ARTIMISIA (NON orientato)--------------------------------------------------------------------------------------------------------------------------
def getInfoConnessa(self, idInt):
    # Identifica la componente connessa che contiene idInt e ne restituisce la dimensine
    # tutti i nodi che posso raggiungere da source --> DEPTH FIRST

    if not self.hasNode(idInt):  # ridondante perchè lo facciamo già nel controller
        return None

    source = self._idMap[idInt]  # PRIMA devo verificare che nel grafo (il dict) esiste quel nodo (idInt)

    # Modo 1: conto i successori --> errore: contare il num di valori del dict non è la stessa cosa (conta il num di liste come 1+1+1 invece di n)
    succ = nx.dfs_successors(self._graph, source)  # restituisce un dict: chiave: ogg, valori: lista ogg
    # print(succ)                                    #per ogni nodo ho una lista di nodi dove posso andare
    ris = []
    for s in succ.values():
        ris.extend(s)  # se la riga è un ogg allora aggiunge ogg, se è una lista di ogg, allora aggiunge tutti gli ogg
    print(f"Size componente connessa modo 1: {len(ris)} ")

    # Modo 2: conto i precessori (dovrei comunque ottenere lo stesso numero)
    pre = nx.dfs_predecessors(self._graph, source)
    # print(pre)                                    #per ogni nodo ho un solo valore, c'è solo un padre da cui arrivo
    print(f"Size componente connessa modo 2: {len(pre.values())} ")

    # Modo 3: conto i nodi dell'albero di visita --> mi da metodo 2(+1 perchè conta anche source)
    dfsTree = nx.dfs_tree(self._graph, source)
    print(f"Size componente connessa modo 3: {len(dfsTree.nodes())} ")

    # Modo 4: uso il metodo di networkx
    # ritorna il set di nodi nella componente del grafo che contiene il nodo n
    conn = nx.node_connected_component(self._graph, source)
    print(f"Size componente connessa modo 4: {len(conn)} ")

    #Modo 5: numero (NON orientato)
    def getNumComponentiConnesse(self):
        return nx.number_connected_components(self._graph)
    return len(conn)

#Metro-Paris--------------------------------------------------------------------------------------------------------------------------------
#VISITA GRAFI
#       -Sapere quali NODI visito (ordine) -->	getBFSnodesFromTree, getDFSnodesFromTree
#       -Sapere quali ARCHI compongono l’albero di visita --> usare direttamente nx.bfs_edges, nx.dfs_edges


    def getBFSnodesFromTree(self, source): #tutti i nodi

        #Breadth-first-visit --> visita per livelli (ampiezza)
        tree = nx.bfs_tree(self._grafo, source)
        archi = list(tree.edges())
        nodi = list(tree.nodes())
        return nodi[1:]
        #return lista di nodi


    def getDFSnodesFromTree(self, source): #tutti i nodi

        #Depth-first-visit --> visita in profindità
        tree= nx.dfs_tree(self._grafo, source)
        nodi= list(tree.nodes())
        return nodi[1:] #per togliere il nodo da cui parto
        #return lista di nodi

    def getBFSnodesFromEdges(self, source):           #solo figli trovati

        archi = nx.bfs_edges(self._grafo, source) #return iteratore di tuple: coppia (padre-figlio) di archi --> [('A', 'B'), ('A', 'C'), ('B', 'D')]
        ris = []
        for nodoPartenza, nodoArrivo in archi:
            ris.append(nodoArrivo)
        return ris
        #return --> lista di nodi figli visitati in ordine di espansione


    def getDFSnodesFromEdges(self, source):             #solo figli trovati

        archi = nx.dfs_edges(self._grafo, source)
        ris = []
        for nodoPartenza, nodoArrivo in archi:
            ris.append(nodoArrivo)
        return ris
        #return --> lista dei nodi figli visitati

#Vari modi per verificare la connettività (Lab10)
    #1° NetworkX --> già pronto
    def getStatiRaggiungibili1(self, stato):
        return list(nx.node_connected_component( self._graph, stato))

    #2° DFS o BFS
    def getNodiRaggiungibiliDFS(self, statoSource):

        alberoStatiRaggiungibili = nx.dfs_tree(self._graph, statoSource) #GRAFO ORIENTATO
        statiRaggiungibili= alberoStatiRaggiungibili.nodes()
        return statiRaggiungibili

    #3° ITERATIVO
    def getNodiRaggiungibiliIterativo(self, statoSource):

        from collections import deque

        daVisitare = deque()            #lista: permette di aggiungere e rimuovere elementi da entrambi gli estremi in modo efficiente
        visitati = []

        visitati.append(statoSource)    #aggiunto il nodo iniziale nella lista di quelli visitati
        daVisitare.extend(self._graph.neighbors(statoSource))

        while len(daVisitare) > 0:
            ultimo = daVisitare.popleft()                 #prendi l'ultimo nodo inserito
            visitati.append(ultimo)

            vicini = list(self._graph.neighbors(ultimo))  #vicini di questo nodo

            #Remove from this list the elements that are already in "visitati" e "daVisitare"
            vicini_filtrati= []

            for vicino in vicini:
                if vicino not in visitati:
                    vicini_filtrati.append(vicino)
                elif vicino not in daVisitare:
                    vicini_filtrati.append(vicino)

            # Add the remaining to the queue of those to be visited
            daVisitare.extend(vicini_filtrati)

        visitati.remove(statoSource)
        return visitati

            # nodo=daVisitare.pop()
            # if nodo not in visitati:    #se non l'hai già visitato allora aggiungilo alla lista
            #     visitati.append(nodo)
            #     for vicino in self._graph.neighbors(nodo): #per ogni vicino del nodo, aggiungilo alla lista DAvisitare se già non c'è
            #         if vicino not in visitati:
            #             daVisitare.append(vicino)
            # visitati.remove(nodo)


        return visitati

    #4° RICORSIVO
    def getNodiRaggiungibiliRicorsivo(self, statoSource):

        visitati=[]
        self._ricorsivo(statoSource, visitati)
        visitati.remove(statoSource)
        return visitati

    def _ricorsivo(self, statoSource, visitati):

        visitati.append(statoSource)
        #Iterare su tutti i vicini dello stato
        for stato in self._graph.neighbors(statoSource):
            #FILTRO: visita n solo se non è già stato visitato ancora
            if stato not in visitati:
                self._ricorsivo(stato, visitati)