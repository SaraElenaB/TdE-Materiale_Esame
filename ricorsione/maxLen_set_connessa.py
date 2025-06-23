#TdE-iTunes
Permettere all’utente di inserire una durata complessiva dTOT, espressa in minuti. Alla pressione del bottone “Set di Album”, utilizzare un algoritmo ricorsivo per estrarre un set di album dal grafo che abbia le seguenti caratteristiche:
• includa a1;
• includa solo album appartenenti alla stessa componente connessa di a1;
• includa il maggior numero possibile di album;
• abbia una durata complessiva, definita come la somma della durata degli album in esso contenuti, non superiore dTOT.

#PUNTO 2:
    def getSetOfNodes(self, a1, dTot):

        self._bestSet = set()
        self._maxLen = 0
        parziale = set()

        # set parziale --> sicuro non aggiungo doppioni
        # remove --> togliere gli elementi che ho già inserito, non ha senso tenerla nella cc

        parziale.add(a1)
        cc = nx.node_connected_component(self._grafo, a1)
        cc.remove(a1)

        for n in set(cc): #crei una copia
            parziale.add(n)
            cc.remove(n)
            self._ricorsione( parziale, cc, dTot) #a1 --> è gia in parziale
            cc.add(n)
            parziale.remove(n)

        return self._bestSet, self._getDurataComplessiva(self._bestSet)

    # --------------------------------------------------------------------------------------------------------------------------------
    def _ricorsione(self, parziale, rimanenti, dTot):

        # terminale: #ammissibile? --> viola i vincoli?
        if self._getDurataComplessiva(parziale) > dTot:
            return

        # se non ammissibile --> è migliore?
        if len(parziale) > self._maxLen:
            self._maxLen = len(parziale)
            self._bestSet = copy.deepcopy(parziale)

        # continuo senza return, aggiungo --> e continuo con ricorsione
        for n in rimanenti:
            parziale.add(n)
            rimanenti.remove(n)
            self._ricorsione(parziale, rimanenti, dTot)
            parziale.remove(n)
            rimanenti.add(n) #backtracking opposto --> serve per andare + veloce