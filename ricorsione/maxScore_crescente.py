#UFO
#cammino di nodi strettamente crescente che massimizzi un punteggio composto dai seguenti termini:
#       • +100 punti per ogni avvistamento nel cammino
#       • +200 punti per ogni avvistamento del cammino che è occorso nello stesso mese dell’avvistamento precedente (non applicabile al primo avvistamento del cammino
#       - massimo 3 avvistamenti dello stesso mese.
#Nota bene: un arco può essere percorso solo nella sua direzione, ovvero un arco diretto da A verso B non può essere percorso da B ad A.

def cammino_ottimo(self):
    self._cammino_ottimo = []
    self._score_ottimo = 0

    for node in self._grafo.nodes():
        parziale = [node]
        rimanenti = self.calcola_rimanenti(parziale)
        self._ricorsione(parziale, rimanenti)

    return self._cammino_ottimo, self._score_ottimo

# ------------------------------------------------------------------------------------------------------------------------------
def _ricorsione(self, parziale, nodi_rimanenti):
    # grafo: per def non ha ciclo
    if len(nodi_rimanenti) == 0:
        punteggio = self.calcola_punteggio(parziale)
        if punteggio > self._score_ottimo:
            self._score_ottimo = punteggio
            self.cammino_ottimo = copy.deepcopy(parziale)
    else:
        for nodo in nodi_rimanenti:
            parziale.append(nodo)
            nuovi_rimanenti = self.calcola_rimanenti(parziale)
            self._ricorsione(parziale, nuovi_rimanenti)
            parziale.pop()


# ------------------------------------------------------------------------------------------------------------------------------
def calcola_rimanenti(self, parziale):
    # nuovi_rimanenti = self._grafo.successors(parziale[-1]) #funzione che dato il grafo (l'ultimo nodo che abbiamo messo nel parziale) --> trova i successivi

    nuovi_rimanenti = []
    # prendiamo i nodi successivi
    for i in self._grafo.successors(parziale[-1]):
        # di questi nodi, dobbiamo verificare il vincolo sul mese
        if (self.is_vincolo_ok(parziale, i) and self.is_vincolo_durata_ok(parziale, i)):
            nuovi_rimanenti.append(i)
    return nuovi_rimanenti

# ------------------------------------------------------------------------------------------------------------------------------
def is_vincolo_durata_ok(self, parziale, nodo: Sighting):
    return nodo.duration > parziale[-1].duration  # strettamente crescente

# ------------------------------------------------------------------------------------------------------------------------------
def is_vincolo_ok(self, parziale, nodo: Sighting):  # trucco, se dici che nodo è un ogg Sightinh così poi ti aiuta dopo

    mese = nodo.datetime.month
    counter = 0
    for i in parziale:
        if i.datetime.month == mese:
            counter += 1
    if counter >= 3:
        return False
    else:
        return True

# ------------------------------------------------------------------------------------------------------------------------------
def calcola_punteggio(self, parziale):
    punteggio = 0

    # termine fisso
    punteggio += 100 * len(parziale)
    # termine variabile
    for i in range(1, len(parziale)):  # escludiamo il primo
        nodo = parziale[i]
        nodo_precedente = parziale[i - 1]
        if nodo.datetime.month == nodo_precedente.datetime.month:
            punteggio += 200

    return punteggio