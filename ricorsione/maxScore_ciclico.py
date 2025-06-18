#Dato il grafo costruito al punto precedente, si vuole identificare un percorso semplice e chiuso a peso massimo
#     -composto da esattamente N archi --> N utente e >= 2
#     -sequenza di vertici con_
#           -Il primo e l’ultimo vertice devono coincidere
#           -intermedi non devono essere ripetuti
#           -La somma dei pesi degli archi percorsi deve essere massima

def getCamminoOttimo(self, numArchiMax):
    self._bestPath = []
    self._bestCost = 0
    parziale = []

    for nodo in self._nodes:
        parziale.append(nodo)
        self._ricorsione(parziale, numArchiMax)
        parziale.pop()

    return self._bestPath, self._bestCost


# ----------------------------------------------------------------------------------------------------------------------------------
def _ricorsione(self, parziale, numArchiMax):
    # è ammissibile?
    if len(parziale) == numArchiMax + 1:  # archi = nodo+1
        if parziale[0] == parziale[-1]:
            # è la migliore?
            costo = int(self.getCosto(parziale))
            if costo > self._bestCost:
                print(f"Soluzione migliore trovata")
                self._bestCost = costo
                self._bestPath = copy.deepcopy(parziale)
    else:
        # continua a cercare il migliore --> ricorsione
        ultimo = parziale[-1]
        for n in self._grafo.neighbors(ultimo):
            # vincoli
            if n == parziale[0] and len(parziale) == numArchiMax:
                parziale.append(n)
                self._ricorsione(parziale, numArchiMax)
                parziale.pop()

            elif n not in parziale:
                print(f"Ricorsione: {parziale}")
                parziale.append(n)
                self._ricorsione(parziale, numArchiMax)
                parziale.pop()


# ----------------------------------------------------------------------------------------------------------------------------------
def getCosto(self, listaNodi):
    print("called funzione costo"
          "")
    costo = 0
    for i in range(len(listaNodi) - 1):
        if self._grafo.has_edge(listaNodi[i], listaNodi[i + 1]):
            costo += self._grafo[listaNodi[i]][listaNodi[i + 1]]["weight"]
    return costo

