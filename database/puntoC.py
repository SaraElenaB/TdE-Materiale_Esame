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

#TdE-iTunes: -------------------------------------------------------------------------------------------------------------------------------------------------
#“Analisi Componente”, si stampino:
#   -la dimensione della componente connessa a cui appartiene a1;
#   -la durata complessiva (in minuti) di tutti gli album appartenenti alla componente connessa di a1
    def getInfoConnessa(self, a1):

        #grafo NON orientato
        nodiConnessi = nx.node_connected_component(self._grafo, a1)
        durataComplessiva = self._getDurataComplessiva(nodiConnessi)
        return len(nodiConnessi), durataComplessiva

    def _getDurataComplessiva(self, listaNodi):

        sumDurata=0
        for n in listaNodi:
            sumDurata += n.dTotMin
        return sumDurata

#TdE-Gene_small: -------------------------------------------------------------------------------------------------------------------------------------------------
#Si visualizzi i valori minimo e massimo dei pesi degli archi.
# Permettere all’utente di inserire un valore soglia (S), verificando che tale valore sia compreso nell’intervallo minimo-massimo calcolato al punto d.
#. Alla pressione del bottone “Conta archi” stampare il numero di archi il cui peso è <S, ed il numero di archi il cui peso è >S.
    def getMinPeso(self):

        min=float('inf') #1000000000000000000000
        for edge in self._grafo.edges( data=True):
            if edge[2]["weight"] < min:
                min = edge[2]["weight"]
        return min

    def getMaxPeso(self):

        max=float('-inf') #-100000000000000000
        for edge in self._grafo.edges( data=True):
            if edge[2]["weight"] > max:
                max = edge[2]["weight"]
        return max

    # ------------------------------------------------------------------------------------------------------------------------------------
    def getArchiSoglia(self, soglia):

        if soglia > self.getMaxPeso() and soglia < self.getMinPeso():
            return f"Attenzione, valore della soglia non valido!"

        numArchiMinoreSoglia = 0
        numArchiMaggioreSoglia = 0
        for edge in self._grafo.edges( data=True):
            weight = edge[2]["weight"]
            if weight < soglia:
                numArchiMinoreSoglia += 1
            elif weight > soglia:
                numArchiMaggioreSoglia += 1

        return numArchiMinoreSoglia, numArchiMaggioreSoglia