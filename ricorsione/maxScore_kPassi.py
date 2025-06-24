#TdE-Flight_delays
#a. seleziona aeroporto di destinazione a2, e un numero massimo di tratte t che è disposto a percorrere.
#b. viaggio tra a1 (selezionato) e a2 (selezionato) che massimizzi la somma dei pesi degli archi attraversati utilizzando al massimo t tratte.
#c. stampare l’itinerario, indicando gli aeroporti visitati, e il numero totale di voli disponibili sul percorso.

def getCamminoOttimo(self, aeroportoP, aeroportoA, maxTratte):
    self._bestPath = {}  # durante la ricorsione salviamo il migliore
    self._bestScore = 0  # somma dei costi
    parziale = [aeroportoP]  # vettore su cui lavoriamo
    self._ricorsione(parziale, aeroportoA, maxTratte)
    return self._bestPath, self._bestScore


# -----------------------------------------------------------------------------------------------------------------------------------------
def _ricorsione(self, parziale, aeroportoA, maxTratte):  # per capire se siamo arrivati alla fine
    # verificare se parziale è una possibile soluzione
    # verificare se è il migliore

    # terminale:
    if parziale[-1] == aeroportoA:
        if len(parziale) <= maxTratte:
            if self.getBestScore(parziale) > self._bestScore:
                self._bestScore = self.getBestScore(parziale)
                self._bestPath = copy.deepcopy(parziale)
    if len(parziale) > maxTratte:
        return

    # ricorsione --> posso ancora aggiungere nodi, partendo dall'ultimo nodo e prendo i vicini aggiungendo un nodo alla volta e rifaccio partire la ricorsione
    for n in self._grafo.neighbors(parziale[-1]):
        # vincolo --> controllo che non sia gia stato visitato
        if n not in parziale:
            parziale.append(n)
            self._ricorsione(parziale, aeroportoA, maxTratte)  # se torno indietro vuol dire che l'ho già visto
            parziale.pop()


# -----------------------------------------------------------------------------------------------------------------------------------------
def getBestScore(self, listaDiNodi):
    # percorso che massimizzi la somma dei pesi degli archi attraversati
    totPesi = 0
    for i in range(0, len(listaDiNodi) - 1):
        totPesi += self._grafo[listaDiNodi[i]][listaDiNodi[i + 1]]["weight"]
    return totPesi