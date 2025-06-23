#TdE-Gene_small
#a. determinare il più lungo cammino di vertici (cromosomi) che sia composto esclusivamente da archi di peso >S. La lunghezza del cammino sarà valutata dalla somma dei pesi degli archi incontrati.
#b. Si stampi la sequenza di cromosomi di lunghezza massima così ottenuta.
def getCamminoOttimo(self, soglia):
    self._bestPath = []
    self._bestScore = 0
    parziale = []

    for nodo in self._grafo.nodes:
        parziale.append(nodo)
        self._ricorsione(parziale, soglia)
        parziale.pop()

    ris = []
    for i in range(0, len(self._bestPath) - 1):
        ris.append(
            (self._bestPath[i], self._bestPath[i + 1], self._grafo[self._bestPath[i]][self._bestPath[i + 1]]["weight"]))

    return ris, self._bestScore


# ------------------------------------------------------------------------------------------------------------------------------------
def _ricorsione(self, parziale, soglia):
    # ammissibile? controllo dopo
    # migliore?
    costo = self.calcolaScore(parziale)
    if costo > self._bestScore:
        print(f"Soluzione migliore trovata")
        self._bestScore = costo
        self._bestPath = copy.deepcopy(parziale)

    # continua la ricerca per vedere se c'è un migliore
    ultimo = parziale[-1]
    for vicino in self._grafo.neighbors(ultimo):  # controlli cammini reali
        # vincoli
        if not self.arcoGiaConsiderato(ultimo, vicino, parziale) and (
                (self._grafo[ultimo][vicino]["weight"] > soglia)):
            print(f"Parziale: {parziale}")
            parziale.append(vicino)
            self._ricorsione(parziale, soglia)
            parziale.pop()


# ------------------------------------------------------------------------------------------------------------------------------------
def calcolaScore(self, listaNodi):
    print(f"Called function score")
    peso = 0
    for i in range(0, len(listaNodi) - 1):
        peso += self._grafo[listaNodi[i]][listaNodi[i + 1]]["weight"]
    return peso


def arcoGiaConsiderato(self, n1, n2, listaNodi):
    for i in range(0, len(listaNodi) - 1):
        if (n1, n2) == (listaNodi[i], listaNodi[i + 1]):
            return True
    return False

#RICORSIONE 2: al posto di .neighbors() usa DFS
    #grafo NON orientato--------------------------------------
    # for component in nx.connected_components(self._grafo):
    #     nodo_iniziale = next(iter(component))
    #     for u, v in nx.dfs_edges(self._grafo, source=nodo_iniziale):

    # #grafo ORIENTATO-------------------------------------------
    # for component in nx.weakly_connected_components(self._grafo):
    #     nodo_iniziale = next(iter(component))
    #     for u, v in nx.dfs_edges(self._grafo, source=nodo_iniziale):

    # #nodo INIZIALE---------------------------------------------
    # edges_dfs = list(nx.dfs_edges(self._grafo, source=a1))
    # for u, v in edges_dfs:
    #     # puoi fare controlli su u-v come arco, oppure costruire un cammino
    #     if some_condition(u, v):
    #         parziale.append(v)
    #         self._ricorsione(parziale, soglia)
    #         parziale.pop()