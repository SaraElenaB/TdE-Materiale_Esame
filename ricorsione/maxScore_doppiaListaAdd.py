def getCamminoOttimo(self, nodoPartenza: Product):
    # percorso più lungo con nodi che hanno peso crescente

    self._bestPath = []
    self._bestSolution = 0  # num di archi attraversati
    archiUsati = set()
    parziale = [nodoPartenza]
    self._ricorsione(parziale, [], 0, archiUsati)
    return self._bestPath


# ------------------------------------------------------------------------------------------------------------------------------
def _ricorsione(self, parziale: list, parzialeArchi: list, peso_precedente: int, archi_usati: set()):
    # terminale
    if len(parzialeArchi) > len(self._bestPath):
        self._bestPath = copy.deepcopy(parzialeArchi)

    # ricorsione
    ultimo = parziale[-1]
    for vicino in self._grafo.neighbors(ultimo):

        # per togliere (nodo1, nodo2) diverso (nodo2, nodo1)
        archiOrdinati = tuple(sorted((vicino, ultimo), key=lambda nodo: nodo.Product_number))
        if archiOrdinati not in archi_usati:
            peso = self._grafo[vicino][ultimo]["weight"]
            if peso > peso_precedente:
                parziale.append(vicino)
                archi_usati.add(archiOrdinati)
                parzialeArchi.append(archiOrdinati)

                self._ricorsione(parziale, parzialeArchi, peso, archi_usati)
                parziale.pop()
                parzialeArchi.pop()
                archi_usati.remove(archiOrdinati)