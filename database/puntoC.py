#LAB14: il cammino più lungo partendo da un nodo. Il nodo è selezionato dall’apposito menù a tendina.
def getLongestPath(self, nodoId):

    source = self._mapNodes[int(nodoId)]
    self._longestPath = []
    parziale = [source]
    nodi = list( nx.dfs_tree(self._grafo, source))
    self._ricorsione1(parziale, nodi)
    return self._longestPath

def _ricorsione1(self, parziale, nodi):
    #terminale
    if len(parziale) > len(self._longestPath):
        self._longestPath = copy.deepcopy(parziale)

    #ricorsione
    for node in nodi:
        if node not in parziale:
            parziale.append(node)
            self._ricorsione1(parziale, nodi)
            parziale.pop()

#-------------------------------------------------------------------------------------------------------------------------------------------------
#LAB12:“volume di vendita” --> di un retailer la somma dei pesi di tutti gli archi ad esso incidenti, ordinati per valore decrescente
def getInfoVolumeVendita(self):

    listTuple=[]
    for nodo in self._grafo.nodes:
        volume = 0
        for vicino in self._grafo.neighbors(nodo):
            volume += self._grafo[nodo][vicino]["weight"]
        listTuple.append( (nodo, volume) )

    listTuple.sort( key = lambda x: x[1] , reverse=True )
    return listTuple

#-------------------------------------------------------------------------------------------------------------------------------------------------
#LAB13: Costruito il grafo, l’applicazione visualizza il pilota che ha totalizzato il miglior risultato, definito come
# differenza tra il numero di vittorie (archi uscenti) e di sconfitte (entranti)
# -grafo orientato -->succ e pre hanno senso
    def getBestScore(self):

        bestScore = 0
        bestPilota = None

        for nodo in self._grafo.nodes():
            pesoVittorie = 0
            pesoSconfitte = 0

            for succ in self._grafo.successors(nodo):
                pesoVittorie += self._grafo[nodo][succ]["weight"]
            for pre in self._grafo.predecessors(nodo):
                pesoSconfitte += self._grafo[pre][nodo]["weight"]

            score = pesoVittorie - pesoSconfitte
            if score > bestScore:
                bestScore = score
                bestPilota = nodo.surname

        return bestPilota, bestScore