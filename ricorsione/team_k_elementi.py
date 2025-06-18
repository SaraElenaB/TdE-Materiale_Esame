#a. Facendo click sul pulsante “DreamTeam”, individuare un dream team.
#b. Definiamo come team un gruppo di K piloti.
#       -La dimensione K del team viene stabilita dall’utente con l’apposita casella di testo.
#c. Il tasso di sconfitta di un team è definito come:
#        il numero totale di vittorie di un qualsiasi pilota non appartenente al team su un qualsiasi pilota appartenente al team.
#d. Un dream team è un team di K piloti che abbia il minimo tasso di sconfitta
import copy

#Lab13
def getDreamTeam(self, numPiloti):
    self.bestPath = []
    self.bestTassoSconfitta = 100000
    parziale = []
    self._ricorsione(parziale, numPiloti)
    return self.bestPath, self.bestTassoSconfitta

    # ATTENZIONE --> con il metodo sotto ottieni delle permutazioni ("A","B" diverso da "B","A")
    #           --> fai delle combinazioni direttamente nella ricorsione
    # for node in self._nodes:
    #     parziale.append(node)
    #     self._ricorsione( parziale, numPiloti)
    #     parziale.pop()


# --------------------------------------------------------------------------------------------------------------------------------------------
def _ricorsione(self, parziale, numPiloti):
    # è ammissibile?
    if len(parziale) == numPiloti:
        # è la migliore?
        print(f"Testing team")
        tasso = self.calcolaTassoSconfitta(parziale)
        if tasso < self.bestTassoSconfitta:
            print(f"Soluzione migliore trovata")
            self.bestTassoSconfitta = tasso
            self.bestPath = copy.deepcopy(parziale)
        return

    else:
        # continua a cercare altre opzioni
        for node in self._nodes:
            if node not in parziale:
                print(f"Ricorsione: {parziale}")
                parziale.append(node)
                self._ricorsione(parziale, numPiloti)
                parziale.pop()


# --------------------------------------------------------------------------------------------------------------------------------------------
def calcolaTassoSconfitta(self, listaNodi):
    print("called funzione tasso")
    # 2 --> archi
    tasso = 0
    for edge in self._grafo.edges(data=True):
        if edge[0] not in listaNodi and edge[1] in listaNodi:  # arco( noTeam-Team) = vittoria
            tasso += self._grafo[edge[2]]["weight"]
    return tasso

    # 2 --> NODO
    # tasso=0
    # for n in self._nodes:
    #     for p in listaNodi:
    #         if n not in listaNodi:
    #             if self._grafo.has_edge(n, p):
    #                 tasso += self._grafo[n][p]["weight"] #arco escluso--team: vittoria
    # return tasso
