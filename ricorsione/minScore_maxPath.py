#TdE_Gene_small2
#cammino più lungo che minimizza la somma dei pesi del percorso, e con le seguenti caratteristiche:
#       -I. nodo attraversato una sola volta.
#       -II. Gli archi solo nella loro direzione di percorrenza
#       -III. non ci possono essere due geni consecutivi con lo stesso valore del campo Essential
#       -IV. archi di peso crescente (nuovo peso >= del precedente)
#In seconda istanza, tra i diversi  cammini di pari lunghezza, dovrà prediligere il percorso a peso totale minimo.
#Si stampino:
#       -I. Il numero di nodi nel cammino trovato
#       -II. Il peso totale del cammino trovato
#       -III. La sequenza di nodi attraversati

def getCamminoOttimo(self):

        #cammino + lungo con score minore
        self._bestPath=[]
        self._bestScore=float("inf")
        parziale=[]

        for nodo in self._nodes:  #inizio senza escludere tutti i cammini che hanno solo un nodo
            print(f"Inizio da nodo: {nodo} con successori: {list(self._grafo.successors(nodo))}")
            parziale.append(nodo)
            self._ricorsione(parziale)
            parziale.pop()

        if not self._bestPath:
            print("Nessun cammino ammissibile trovato.")

        return self._bestPath, self._bestScore

    def _ricorsione(self, parziale):
        #ammissibile? vincoli
        #migliore?
        #ATTENZIONE!! quando len(parziale)==1 ha score=0 che è il migliore in assoluto, quindi non considerare quel caso
        if len(parziale)>1 and len(parziale) >= len(self._bestPath):
            score = self.calcolaScore(parziale)
            if score < self._bestScore:
                print(f"Soluzione migliore trovata")
                self._bestScore = score
                self._bestPath = copy.deepcopy(parziale)


        ultimo = parziale[-1]
        for succ in self._grafo.successors(ultimo):
            #vincoli
            if succ not in parziale and ultimo.Essential != succ.Essential:
                pesoAttuale = 0
                pesoNuovo = 0

                if len(parziale)==2:
                    pesoAttuale = 0
                    pesoNuovo = self._grafo[ultimo][succ]["weight"]
                if len(parziale)>2:
                    pesoAttuale = self._grafo[parziale[-2]][ultimo]["weight"]
                    pesoNuovo =  self._grafo[ultimo][succ]["weight"]

                if pesoAttuale <= pesoNuovo:
                    print(f"Ricorsione: {parziale}")
                    parziale.append(succ)
                    self._ricorsione(parziale)
                    parziale.pop()
                else:
                    continue
            else:
                continue

    # -------------------------------------------------------------------------------------------------------------------------------
    def calcolaScore(self, listaNodi):

        print(f"Called function calcolaScore")
        pesoTot=0
        for i in range(0, len(listaNodi)-1):
            pesoTot += self._grafo[listaNodi[i]][listaNodi[i+1]]['weight']
        return pesoTot