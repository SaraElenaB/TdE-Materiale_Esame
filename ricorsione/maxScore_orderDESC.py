#Lab14
# Partendo dal grafo ottenuto nel punto precedente, alla pressione del bottone “Ricorsione”, si implementi una
# procedura ricorsiva che calcoli un percorso di peso massimo. Il vertice di partenza è quello selezionato nel punto 1.c
# e il peso degli archi nel percorso deve essere strettamente decrescente.

#MAX PERCORSO CON PESO SEMPRE DESCRESCENTE
def getBestCamminoPesoMaggiore(self, sourceId):

    source = self._mapNodes[int(sourceId)]
    self._bestPath = []
    self._bestCost = 0
    parziale = [source]

    # serve a iniziare il processo con un cammino già con due nodi, così che dentro la ricorsione puoi fare
    # confronti con parziale[-2]parziale[-1]
    vicini = self._grafo.neighbors(source)
    for v in vicini:
        parziale.append(v)
        self._ricorsione2(parziale)
        parziale.pop()

    return self._bestPath, self._bestCost


def _ricorsione2(self, parziale):
    #ammissibile? --> nei vincoli
    #migliore?
    costo = self.calcolaCosto(parziale)
    if costo > self._bestCost:
        self._bestCost = costo
        self._bestPath = copy.deepcopy(parziale)

    # ricorsione --> continua la costruzione del cammino ricorsivamente, ma per funzionare ha bisogno che il cammino abbia
    # almeno 2 nodi per confrontare il peso
    for nodo in self._grafo.neighbors(parziale[-1]):
        # vincoli
        if (nodo not in parziale and
                self._grafo[parziale[-2]][parziale[-1]]["weight"] >
                self._grafo[parziale[-1]][nodo]["weight"]):
            parziale.append(nodo)
            self._ricorsione2(parziale)
            parziale.pop()


# --------------------------------------------------------------------------------------------------------------------------------
def calcolaCosto(self, listaDiNodi):
    costo = 0
    for i in range(len(listaDiNodi) - 1):
        costo += self._grafo[listaDiNodi[i]][listaDiNodi[i + 1]]["weight"]

    return costo

# --------------------------------------------------------------------------------------------------------------------------------
