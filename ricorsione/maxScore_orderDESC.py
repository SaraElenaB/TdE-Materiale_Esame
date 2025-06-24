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

#TdE-Baseball (stessa richiesta, altro modo)
    def getCamminoOttimoV2(self, source):

        self._bestPath = []
        self._bestScore = 0
        parziale = [source]

        vicini = nx.neighbors(self._grafo, source)
        viciniTuple=[]
        for v in vicini:
            peso=self._grafo[source][v]["weight"]
            viciniTuple.append( (v,peso))

        viciniTuple.sort( key=lambda x: x[1], reverse=True)
        #non avendo altri archi --> non devo controlalre che il peso sia minore/maggiore
        parziale.append(viciniTuple[0][0]) #prendo il primo nodo
        self._ricorsioneV2(parziale)
        parziale.pop()
        return self.getPesiOfPath(self._bestPath) , self._bestScore

    # ---------------------------------------------------------------------------------------------------------------------------
    def _ricorsioneV2(self, parziale):
        print(len(parziale))
        # 1. terminale
            # parziale è una soluzione?
            # parziale è meglio della best
        if self.score(parziale) > self._bestScore:  # non ho vincoli sulla lunghezza, ma sul peso
            self._bestPath = copy.deepcopy(parziale)
            self._bestScore = self.score(parziale)

        # 2. #ricorsione
            # posso aggiungere un nuovo nodo?
            # aggiungo nodo e faccio la ricorsione
        vicini = nx.neighbors(self._grafo, parziale[-1])
        viciniTuple = []
        for v in vicini:
            peso = self._grafo[parziale[-1]][v]["weight"]
            viciniTuple.append( (v, peso) )
        viciniTuple.sort(key=lambda x: x[1], reverse=True)

        for t in viciniTuple:
            if ((t[0] not in parziale) and
                    (self._grafo[parziale[-2]][parziale[-1]]["weight"] > t[1])):  # già aggiunto > di quello che aggiiungo
                parziale.append(t[0])
                self._ricorsioneV2(parziale)
                parziale.pop()
                return

    # ---------------------------------------------------------------------------------------------------------------------------
    def score(self, listaDiNodi):

        if len(listaDiNodi) < 2:
            warnings.warn("Errore in score, attesa lista più lunga")

        totPeso=0
        for i in range(len(listaDiNodi)-1):
            totPeso += self._grafo[listaDiNodi[i]][listaDiNodi[i+1]]["weight"]
        return totPeso

    # ---------------------------------------------------------------------------------------------------------------------------
    def getPesiOfPath(self, listaDiNodi):

        tuplePesi= [ (listaDiNodi[0], 0)]
        for i in range(1, len(listaDiNodi)):
            tuplePesi.append( (listaDiNodi[i], self._grafo[listaDiNodi[i-1]][listaDiNodi[i]]["weight"]) )
        return tuplePesi

    # ---------------------------------------------------------------------------------------------------------------------------
    def getRandomNode(self):
        index = random.randint(0,len(self._grafo.nodes)-1)
        return list(self._grafo.nodes)[index]