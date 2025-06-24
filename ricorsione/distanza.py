#TdE-Ufo
Dato il grafo costruito al punto precedente, si vuole identificare un percorso semplice che massimizza la distanza tra
stati con archi con peso sempre crescente.
a. Alla pressione del bottone “Calcola percorso” avviare l’algoritmo di ricerca
b. Stampare a video il percorso con peso di ogni arco e distanza geodesica tra i due stati
c. Hint: Per il calcolo della massima distanza tra stati usare i campi “lat” e “lng” del db

def buildGraph(self):
    # Per il punto 2:
    for e in self._grafo.edges(data=True):
        self._grafo[e[0]][e[1]]["distance"] = self.getDistanzaDueStati(e[0], e[1])

def camminoOttimo(self):
    # massimizza distanza, sempre crescente
    self._bestPath = []
    self._bestDistanza = 0
    parziale = []

    for nodo in self.nodes:
        parziale.append(nodo)
        self._ricorsione(parziale)
        parziale.pop()

    ris = []
    for i in range(0, len(self._bestPath) - 1):
        peso = self._grafo[self._bestPath[i]][self._bestPath[i + 1]]["weight"]
        distanza = self._grafo[self._bestPath[i]][self._bestPath[i + 1]]["distance"]
        ris.append((self._bestPath[i], self._bestPath[i + 1], peso, distanza))

    return self._bestPath, self._bestDistanza, ris


# -------------------------------------------------------------------------------------------------------------------------------------------
def _ricorsione(self, parziale):
    # è ammissibile (crescente --> lo guardi dopo nei vincoli)
    # è la migliore
    distanza = self.getDistanza(parziale)
    if distanza > self._bestDistanza:
        self._bestDistanza = distanza
        self._bestPath = copy.deepcopy(parziale)

    else:
        # continua a cercare
        ultimo = parziale[-1]
        for vicino in self._grafo.neighbors(ultimo):
            # vincoli
            if len(parziale) == 1:  # primo nodo, ha solo 1 arco
                parziale.append(vicino)
                self._ricorsione(parziale)
                parziale.pop()
            else:
                if vicino not in parziale and (self._grafo[ultimo][vicino]["weight"] >
                                               self._grafo[parziale[-2]][parziale[-1]]["weight"]):
                    parziale.append(vicino)
                    self._ricorsione(parziale)
                    parziale.pop()


# -------------------------------------------------------------------------------------------------------------------------------------------
def getDistanza(self, listaNodi):
    distanza = 0
    if len(listaNodi) == 1:
        return 0
    for i in range(0, len(listaNodi) - 1):
        distanza += self._grafo[listaNodi[i]][listaNodi[i + 1]]["distance"]
    return distanza


def getDistanzaDueStati(self, s1, s2):
    coord1 = (s1.Lat, s1.Lng)
    coord2 = (s2.Lat, s2.Lng)
    distanza = geopy.distance.distance(coord1, coord2).km
    return distanza