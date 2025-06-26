#TdE-Nyc_hotspot
#selezionare una località target (t) e di inserire una stringa s (non vuota).
#cammino aciclico semplice che abbia le seguenti caratteristiche:
#   -inizi da una delle località calcolate al punto 1d (scelta in modo casuale) e termini in t;
#   -tocchi il maggior numero di località;
#   -non passi per località il cui nome contenga la sottostringa s.
def getCamminoOttimo(self, stringa, target):
    # esiste cammino + lungo che parte da 1d a t

    self._bestPath = []  # [ loc1, loc2, loc3]
    self._bestScore = 0
    parziale = []

    nodiIniziali = self.getAnalisiGrafo()
    start = nodiIniziali[random.randint(0, len(nodiIniziali) - 1)][0]

    if not nx.has_path(self._grafo, start, target):
        print(f"{start} e {target} non sono connessi.")
        return [], start

    if stringa not in start.Location:
        parziale.append(start)
        self._ricorsione(parziale, target, stringa)
        parziale.pop()

    return self._bestPath, self._bestScore


def _ricorsione(self, parziale, target, stringa):
    # terminale
    if parziale[-1] == target:
        if len(parziale) >= self._bestScore:
            self._bestScore = len(parziale)
            self._bestPath = copy.deepcopy(parziale)
        return
    # ricorsione
    ultimo = parziale[-1]
    for vicino in self._grafo.neighbors(ultimo):
        if vicino not in parziale and stringa not in vicino.Location:
            parziale.append(vicino)
            self._ricorsione(parziale, target, stringa)
            parziale.pop()


def _controllaSringa(self, parziale, stringa):
    if stringa in parziale:
        return True