#Lab13
#Grafo orientato pesato
#NODI: Piloti arrivati al traguardo
query = """ select distinct r.driverId
                    from results r , races r2 
                    where r.raceId = r2.raceId
                    and r.`position` > 0
                    and year(r2.`date`) = %s"""

        cursor.execute(query, (anno,))
        for row in cursor:
            #if "driverId" in idMap:
            ris.append( idMap[row["driverId"]] )

#ARCHI: arco orientato rappresenta la vittoria di un pilota su un altro, con peso pari al numero di gare in cui tale vittoria si è verificata.
query = """ select r1.driverId as d1, r2.driverId as d2, count(*) as vittorie
            from results r1, results r2, races ra
            where r1.raceId = r2.raceId
            and r1.raceId = ra.raceId
            and ra.`year` = %s
            and r1.`position` > 0
            and r2.`position` > 0
            and r1.`position` < r2.`position`
            group by d1, d2"""

#Poi salvi in una tupla --> dall'altra parte ricavi i nodi + peso
for row in cursor:
    ris.append((idMap[row["d1"]],
                idMap[row["d2"]],
                row["vittorie"]))
#modello:
for tupla in DAO.getAllEdgesWeigh(anno, self._mapIdPiloti):
    d1 = tupla[0]
    d2 = tupla[1]
    peso = tupla[2]
    if d1 in self._nodes and d2 in self._nodes and peso > 0: #fondamentale per non generare errori
        self._grafo.add_edge(d1, d2, weight=peso)

#-------------------------------------------------------------------------------------------------------------------------------------------------
#Lab14
#grafo orientato
#NODI: ordini  effettuati nello store selezionato.
query = """ select *
            from orders o 
            where o.store_id = %s"""

        cursor.execute(query, (storeId, ))
        for row in cursor:
            ris.append(Order(**row))

#ARCHI: collega ordini effettuati in un massimo di K giorni.
#        numMax giorni --> utente
#        peso --> somma degli oggetti comprati nei due ordini collegati
query = """ select sum(oi.quantity + oi2.quantity ) as totPeso
                    from order_items oi, order_items oi2 ,
                         (select *
                         from orders o 
                         where o.order_id = %s) as a ,
                         (select *
                         from orders o 
                         where o.order_id = %s) as b 
                         where oi.order_id = a.order_id
                         and oi2.order_id = b.order_id"""

#modello
def buildGraph(self, storeId, intNumGiorniMax):
    self._grafo.clear()
    self.nodes = DAO.getAllNodes(storeId)
    self._grafo.add_nodes_from(self.nodes)

    self._mapNodes = {}
    for n in self.nodes:
        self._mapNodes[n.order_id] = n

    for n1, n2 in itertools.combinations(self.nodes, 2):
        diff_days1 = (n1.order_date - n2.order_date).days
        if 0 < diff_days1 < intNumGiorniMax:
            peso1 = DAO.getAllWeight(n1.order_id, n2.order_id)
            self._grafo.add_edge(n1, n2, weight=peso1[0])  # weight=peso1 --> lista
            # weight=peso1[0] --> int

        diff_days2 = (n2.order_date - n1.order_date).days
        if 0 < diff_days2 < intNumGiorniMax:
            peso2 = DAO.getAllWeight(n2.order_id, n1.order_id)
            self._grafo.add_edge(n2, n1, weight=peso2[0])

    return self._grafo

#modo 2
query = """Select DISTINCT o1.order_id as id1, o2.order_id as id2, count(oi.quantity+ oi2.quantity) as cnt
                from orders o1, orders o2, order_items oi, order_items oi2 
                where o1.store_id=%s
                and o1.store_id=o2.store_id 
                and o1.order_date > o2.order_date
                and oi.order_id = o1.order_id
                and oi2.order_id  = o2.order_id
                and DATEDIFF(o1.order_Date, o2.order_date) < %s
                group by o1.order_id, o2.order_id	"""

        cursor.execute(query, (store,k))

        for row in cursor:
            results.append((idMap[row["id1"]],idMap[row["id2"]], row["cnt"]))

#modello
allEdges = DAO.getEdges(store, k, self._idMap)
for e in allEdges:
     self._graph.add_edge(e[0], e[1], weight=e[2])

#-------------------------------------------------------------------------------------------------------------------------------------------------
#Lab12
#GRAFO: semplice, non orientato e pesato
#NODI: tutti retailer presenti nel database
#a. utente seleziona --> nazione, anno A, tra il 2015 ed il 2018
query = """ select *
                    from go_retailers gr 
                    where gr.Country = %s """
for row in cursor:
    ris.append(Retailer(**row))
#ARCO: se e solo se i due retailer corrispondenti hanno
#      -venduto dei prodotti in comune nel corso dell’anno A
#      -peso --> numero di tali prodotti in comune
query = """ select count( distinct gds1.Product_number) as peso
                    from go_daily_sales gds1 , go_daily_sales gds2
                    where  year(gds1.`Date`) = %s 
                    and year(gds1.`Date`) = year(gds2.`Date`)
                    and gds1.Product_number = gds2.Product_number
                    and gds1.Retailer_code = %s
                    and gds2.Retailer_code = %s
                    having peso >= 1 """
                    #ricordati distinct!!!!!

#MODELLO --> grafo semplice non orientato
for n1, n2 in itertools.combinations(self._nodes, 2):
    peso = DAO.getAllEdgesWeight(anno, n1.Retailer_code, n2.Retailer_code)
    if peso:
        self._grafo.add_edge(n1, n2, weight=peso[0])

#-------------------------------------------------------------------------------------------------------------------------------------------------
#TdE-iTunes
#GRAFO: semplice, non orientato e non pesato
#NODI: ogg Album + aggiungo un info nella classe direttamente (dTotMin)
#       album la cui durata (intesa come somma delle durate dei brani ad esso appartenenti) sia superiore a d
query=""" select a.* , sum(t.Milliseconds)/1000/60 as dTotMin
                  from track t , album a 
                  where t.AlbumId = a.AlbumId
                  group by AlbumId 
                  having dTotMin >= %s"""
                  #puoi farlo perchè fai la group by su una chiave primaria

        cursor.execute(query, (dMin,))
        for row in cursor:
            ris.append( Album(**row)) #aggiungo direttamente alla classe

#ARCHI:
#       -collegati se una canzone a1 e una di a2 sono state inserite da un utente all’interno di  una stessa playlist
#       -album diversi, canzoni diverse, playlist uguale
#1:
#distinc --> rende tutto lento!!
        query = """ select distinct t1.AlbumId as a1, t2.AlbumId as a2
                    from playlisttrack p1, playlisttrack p2, track t1, track t2
                    where t1.TrackId = p1.TrackId
                    and  t2.TrackId = p2.TrackId
                    and p1.PlaylistId = p2.PlaylistId
                    and t1.AlbumId < t2.AlbumId"""
                    # <,> --> toglie i doppioni
                    # distinct --> archi molteplici, stessa coppia in diverse playlist
                    # ricordati di mettere solo nodi --> quindi la durata

        cursor.execute(query,)
        for row in cursor:
            # altrimenti errore perchè nella query ho tutti i possibili archi
            if row["a1"] in idMapAlbum and row["a2"] in idMapAlbum:
                ris.append( (idMapAlbum[row["a1"]],
                            idMapAlbum[row["a2"]]) )

        #modello --> tutti gli archi insieme
        self._allEdges = DAO.getAllEdges(self._idMapAlbum)
        self._grafo.add_edges_from(self._allEdges)

#2:
query = """ select distinct p1.PlaylistId
                    from playlisttrack p1, playlisttrack p2, track t1, track t2 
                    where p1.TrackId = t1.TrackId
                    and p2.TrackId = t2.TrackId
                    and p1.PlaylistId = p2.PlaylistId
                    and t1.AlbumId = %s
                    and t2.AlbumId = %s
                    group by p1.PlaylistId"""

        cursor.execute(query, (a1, a2))
        for row in cursor:
            ris.append( row["PlaylistId"])

        #modello --> iterando con 2 album alla volta
        for a1, a2 in itertools.combinations(self._nodes, 2):
            arco = DAO.getEdgeSingolo(a1.AlbumId, a2.AlbumId)
            if len(arco)>0:
                self._grafo.add_edge(a1, a2)

#-------------------------------------------------------------------------------------------------------------------------------------------------
#TdE-Gene_small
#GRAFO: semplice, orientato, pesato
#NODI: cromosomi (tabella genes) considerando solo i valori diversi da 0)
query = """ select distinct g.Chromosome
                 from genes g 
                 where g.Chromosome > 0 """
cursor.execute(query)
        for row in cursor:
            ris.append( row["Chromosome"])

#ARCO: due c diversi, contengono due geni (uno per cromosoma) nello stesso ordine nella tab i.
#       -#vincoli:
#           1 C + geni
# #         1 G + function
#       -peso --> somma algebrica della correlazione
query = """ select sum(a.pesoSingolo) as pesoTot
                    from (select i.GeneID1 as gene1, i.GeneID2 as gene2, i.Expression_Corr as pesoSingolo
                          from genes g1, genes g2, interactions i 
                          where i.GeneID1 = g1.GeneID
                          and i.GeneID2 = g2.GeneID
                          and g1.Chromosome = %s
                          and g2.Chromosome = %s
                          group by gene1, gene2) as a"""
                    #with distinctChromosomes as
                    #      (SELECT g.Chromosome, g.GeneID
                    #       FROM genes g
                    #       WHERE g.Chromosome != 0)

                    #       SELECT ds1.Chromosome as c1, ds2.Chromosome as c2, sum(DISTINCT i.Expression_Corr) as pesoTot
                    #       FROM distinctChromosomes ds1, distinctChromosomes ds2, interactions i
                    #       WHERE ds1.Chromosome != ds2.Chromosome
                    #       and ds1.GeneID = i.GeneID1
                    #       and ds2.GeneID = i.GeneID2
                    #       group by ds1.c1, ds2.c2

        cursor.execute(query, (c1, c2))
        for row in cursor:
            ris.append(row["pesoTot"])
#modello
for c1 in self._grafo.nodes:
    for c2 in self._grafo.nodes:
        if c1 != c2 and not self._grafo.has_edge(n1, n2):  # tutte le possibilità
            peso = DAO.getEdgeWeighted(c1, c2)
            if peso is not None and peso[0] is not None:  # controlla solo quando ha senso: quindi c'è interazione
                self._grafo.add_edge(c1, c2, weight=peso[0])
return self._grafo

#TdE-Gene 2
# GRAFO:  diretto e pesato
self._genes = DAO.get_all_genes()
self._idMapGenes = {} #{'idGene1': [g1, g2], 'idGene2': [g4, g1], 'key3': []} #= gene, diverse funzioni
    for gene in self._genes:
        if gene.GeneID in self._idMapGenes.keys():
            self._idMapGenes[gene.GeneID].append(gene)
        else:
            self._idMapGenes[gene.GeneID] = [gene]

self._interaction = DAO.get_all_interactions()
# NODI: geni (tabella genes, unica con info Chromosoma) sia tale che Chromosoma min <= Chromosoma <= Chromosoma max (dati)
cursor = cnx.cursor(dictionary=True)
            query = """ SELECT GeneID
                        FROM genes
                        WHERE Chromosome >= %s 
                        AND Chromosome <= %s"""
            cursor.execute(query, (c1, c2))

            for row in cursor:
                id_gene = row["GeneID"]
                if id_gene in idMapGenes:
                    result.extend(idMapGenes[id_gene])  #aggiunge gli elementi della lista singolarmente
                    #ti serve salvare singolarmente oggetti Gene, non liste perchè altrimenti nx non riesce ad aggiungere
                    #in quanto sono liste e non oggetti hashable
# ARCHI: geni diversi, stessa Localizzazione (classification), esiste una interazione tra di loro (Interactions)
# PESO: indice di correlazione dell’interazione fra i due geni (tabella interactions)
# VERSO: uscente dal gene con Cromosoma min ed entrante nel gene con Cromosoma maggiore. stesso cromosoma va gestito aggiungendo entrambi gli archi
query = """ select i.Expression_Corr as peso
                        from interactions i, classification c1, classification c2
                        where i.GeneID1 = %s
                        and i.GeneID2 = %s
                        and c1.GeneID = i.GeneID1
                        and c2.GeneID = i.GeneID2
                        and c1.Localization = c2.Localization"""
            cursor.execute(query, (g1Id, g2Id))

            for row in cursor:
                result.append(row["peso"])

#modello
def buildGraph(self, c1, c2):
    self._grafo.clear()
    self._nodes = DAO.getAllNodes(c1, c2, self._idMapGenes)
    print(len(self._nodes))
    self._grafo.add_nodes_from(self._nodes)

    mapNodi = {}
    for g in self._nodes:
        geneId = g.GeneID
        if geneId not in mapNodi:
            mapNodi[g.GeneID] = [g]
        else:
            mapNodi[g.GeneID].append(g)

    for inter in self._interaction:
        gene1 = mapNodi.get(inter.GeneID1)
        gene2 = mapNodi.get(inter.GeneID2)

        if gene1 is not None and gene2 is not None:
            peso = DAO.getEdgeWeight(inter.GeneID1, inter.GeneID2)
            if peso is not None and len(peso) > 0:
                for g1 in gene1:
                    for g2 in gene2:
                        if g1.GeneID != g2.GeneID:
                            if g1.Chromosome < g2.Chromosome:
                                self._grafo.add_edge(g1, g2, weight=peso[0])
                            elif g1.Chromosome > g2.Chromosome:
                                self._grafo.add_edge(g2, g1, weight=peso[0])
                            elif g1.Chromosome == g2.Chromosome:
                                self._grafo.add_edge(g1, g2, weight=peso[0])
                                self._grafo.add_edge(g2, g1, weight=peso[0])

    return self._grafo

#-------------------------------------------------------------------------------------------------------------------------------------------------
#TdE-Ufo
#GRAFO: semplice, NON orientato, pesato
#NODI: tutti gli stati presenti nella tabella “state”.
query = """ select *
                    from state s  """

        cursor.execute(query)
        for row in cursor:
            ris.append( State(**row))

#ARCO: collega due stati solo se sono confinanti
#       -peso: calcolato come il numero di avvistamenti che hanno la stessa forma e stesso anno
query = """ SELECT n.state1, n.state2 , count(*) as peso
                    FROM sighting s , neighbor n 
                    where year(s.`datetime`) = %s
                    and s.shape = %s
                    and (s.state = n.state1 or s.state = n.state2 )
                    and n.state1 < n.state2
                    group by n.state1 , n.state2 """


        cursor.execute(query, ( anno, shape ))
        for row in cursor:
            ris.append( ( row["state1"],
                          row["state2"],
                          row["peso"] ))

#modello
for t in DAO.getAllEdgesWeightMio(anno, shape):
    stato1 = self._idMapStates[t[0]]
    stato2 = self._idMapStates[t[1]]
    peso = t[2]

    if peso > 0:
        self._grafo.add_edge(stato1, stato2, weight=peso)

#TdE-Ufo 2
#GRAFO: orientato e pesato
#NODI: avvistamenti (sighting) nell’anno selezionato e forma
        query = """SELECT *
                   FROM sighting s 
                   WHERE Year(s.datetime)=%s AND s.shape =%s
                   ORDER BY s.longitude ASC"""
        cursor.execute(query, (year, shape,))

        for row in cursor:
            result.append(Sighting(**row))

#ARCO: stesso stato, uscente dall’avvistamento che è avvenuto in una località con Longitudine minore ed entrante nella località a Longitudine maggiore
#PESO: differenza in Longitudine tra nodo di arrivo e nodo di partenza.
#       -Esempio. Se nodo A ha Longitudine -123.0 e nodo B ha longitudine -47 l’eventuale arco sarà diretto da A verso B ed avrà peso 76
        cursor = conn.cursor(dictionary=True)
        query = """select t1.id as id1, abs(t1.longitude) as l1, t2.id as id2, abs(t2.longitude) as d2
                            from (select * from sighting s where YEAR(`datetime`) = %s and shape = %s) t1 ,
                            (select * from sighting s where YEAR(`datetime`) = %s and shape = %s) t2
                            where t1.state = t2.state and abs(t1.longitude) < abs(t2.longitude)
                            order by t1.longitude, t2.longitude"""

        cursor.execute(query, (year, shape, year, shape))

        for row in cursor:
            result.append((idMap[row['id1']], idMap[row['id2']]))
#modello
        # calcolo degli edges in modo programmatico
        for i in range(0, len(self._nodes) - 1):
            for j in range(i + 1, len(self._nodes)):
                if self._nodes[i].state == self._nodes[j].state and self._nodes[i].longitude < self._nodes[j].longitude:
                    weight = self._nodes[j].longitude - self._nodes[i].longitude
                    self._grafo.add_edge(self._nodes[i], self._nodes[j], weight=weight)
                elif self._nodes[i].state == self._nodes[j].state and self._nodes[i].longitude > self._nodes[j].longitude:
                    weight = self._nodes[i].longitude - self._nodes[j].longitude
                    self._grafo.add_edge(self._nodes[j], self._nodes[i], weight=weight)

#-------------------------------------------------------------------------------------------------------------------------------------------------
#TdE-baseball (30/06/23)
    def getPlayerPerYear(nomeSquadra, year):
        query = """ select distinct a.playerID
                    from appearances a , teams t 
                    where t.name = %s
                    and t.teamCode = a.teamCode
                    and a.`year` = %s"""
        #SELECT a.year, GROUP_CONCAT(DISTINCT a.playerID ORDER BY a.playerID) AS players
        # FROM appearances a
        # JOIN teams t ON a.teamCode = t.teamCode
        # WHERE t.name = 'Baltimore Orioles'
        # GROUP BY a.year
        # ORDER BY a.year

#-------------------------------------------------------------------------------------------------------------------------------------------------
#TdE-baseball 7/11/2023
# dd --> anno di campionato, a partire dal 1980
# text1 --> stampare il numero di squadre che ha giocato in tale anno, e l’elenco delle rispettive sigle, completa il dd
# GRAFO: completo, NON ordinato, pesato
# NODI: le squadre di cui al punto precedente
query = """ select *
                    from teams t
                    where t.`year` = %s"""
        cursor.execute(query, (anno,))

        for row in cursor:
            ris.append( Teams(**row))
# ARCHI: colleghino tutte le coppie distinte di squadre.
# PESO: corrisponde alla somma dei salari dei giocatori delle due squadre nell’anno considerato.
ris = {}
        cursor = conn.cursor(dictionary=True)

        query = """ select t.teamCode, t.ID sum(s.salary) as salarioTotSquadra
                    from salaries s , appearances a , teams t 
                    where s.`year` = 2015
                    and s.`year` = a.`year`
                    and s.`year` = t.`year`
                    and a.teamID = t.ID
                    and a.playerID = s.playerID
                    group by t.teamCode, t.name"""
        cursor.execute(query, (anno,))
        # essenzialmente devo collegare Salary e Teams e lo faccio tramite Appearances -->
        # prendi i dati dalle tabelle che hanno sicuramente tutti i valori!!!

        for row in cursor:
            ris[idMapSalari[row["ID"]]] = row["salarioTotSquadra"]

#modello
for n in self._nodes:
    self._idMapSquadreEffettive[n.ID] = n

#ho fatto una mappa come ris del DAO --> { IdSquadra1: salario, IdSquadra2: salario}
        # peso --> somma salario s1 e s2
        salarioDelleSquadre = DAO.getSalarioGiocatoriSquadra(anno, self._idMapSquadreEffettive)
        for e in self._grafo.edges:
            self._grafo[e[0]][e[1]]["weight"] = salarioDelleSquadre[e[0]] + salarioDelleSquadre[e[1]]


#-------------------------------------------------------------------------------------------------------------------------------------------------
#TdE-Flight_Delays 2/07/2018
# GRAFO: semplice, non orientato e pesato
cursor = conn.cursor(dictionary=True)

        query = """SELECT * 
                    from airports a 
                    order by a.AIRPORT asc"""
        cursor.execute(query)

        for row in cursor:
            result.append(Airport(**row))

#modello--> nell'init
self._idMapAirports={}
        for a in self._airports:
            self._idMapAirports[a.ID]=a
# NODI: aeroporti su cui operano almeno x compagnie aeree (in arrivo o in partenza)
#1
query = """select t.ID, t.IATA_CODE, count(*) as numCompagnie
                   from (select a.ID, a.IATA_CODE, f.AIRLINE_ID, count(*) as numVoli
                         from airports a , flights f 
                         where a.ID = f.ORIGIN_AIRPORT_ID or a.ID = f.DESTINATION_AIRPORT_ID
                         group by a.ID, a.IATA_CODE, f.AIRLINE_ID) as t
                   group by t.ID, t.IATA_CODE
                   having numCompagnie>=%s
                   order by numCompagnie asc"""
cursor.execute(query, (minCompagnie,))
        for row in cursor:
            result.append(idMapAirports[row["ID"]])

#2
query=""" select all_airport.id, count(distinct all_airport.airline_id) as numCompagnie
          from (select f.ORIGIN_AIRPORT_ID as id, f.AIRLINE_ID
		        from flights f 
		        group by f.ORIGIN_AIRPORT_ID , f.AIRLINE_ID
                union 
                select f.DESTINATION_AIRPORT_ID as id, f.AIRLINE_ID
                from flights f 
                group by f.DESTINATION_AIRPORT_ID , f.AIRLINE_ID) as all_airport
        group by all_airport.id
        having numCompagnie >= %
        order by all_airport.id"""

# ARCHI:  rotte tra gli aeroporti collegati tra di loro da almeno un volo.
# PESO: numero totale di voli tra i due aeroporti (poiché il grafo non è orientato, considerare tutti i voli in entrambe le direzioni: A->B e B->A)
query = """ select f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID, count(*) as numVoli
                    from flights f 
                    group by f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID
                    order by f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID """
for row in cursor:
    # result.append(idMapAirports[row["ORIGIN_AIRPORT_ID"]],
    #               idMapAirports[row["DESTINATION_AIRPORT_ID"]],
    #               row["numVoli"] )
    result.append(Arco(idMapAirports[row["ORIGIN_AIRPORT_ID"]],
                       idMapAirports[row["DESTINATION_AIRPORT_ID"]],
                       row["numVoli"]))

#arco
@dataclass
class Arco:
    aeroportoP: Airport
    aeroportoA: Airport
    peso: int

#modello
    def addAllArchiPython(self):
        # DAO --> prende tutto
        allEdges= DAO.getAllEdgesPython(self._idMapAirports)
        for e in allEdges:
            if e.aeroportoP in self._grafo and e.aeroportoA in self._grafo: #devo filtrare e aggiungere archi solo dove i nodi ci sono
                if self._grafo.has_edge(e.aeroportoP, e.aeroportoA):
                    self._grafo[e.aeroportoP][e.aeroportoA]["weight"] += e.peso  #se c'è già sommo il peso
                else:
                    self._grafo.add_edge( e.aeroportoP, e.aeroportoA, weight=e.peso )

#-------------------------------------------------------------------------------------------------------------------------------------------------
#TdE-Artimisia --> ARCO!!!!!
#GRAFO: semplice, NON orientato, pesato
#NODI: tutti gli ogg
#ARCHI: 2 ogg contemporaneamente esposti
        # PESO: num di esposizioni contemporaneamente

        query = """select eo.object_id as o1, eo2.object_id as o2, count(*) as peso
                   from exhibition_objects eo , exhibition_objects eo2 
                   where eo.exhibition_id = eo2.exhibition_id
                   and eo.object_id < eo2.object_id 
                   group by eo.object_id, eo2.object_id
                   order by peso desc"""
                   #in questo modo diminuisco la complessità, necessito di rinominare i select perchè li devo usare

        cursor.execute(query, )

        for row in cursor:
            ris.append( Arco( idMap[row["o1"]],
                              idMap[row["o2"]],
                              row["peso"]))

        cursor.close()
        conn.close()

        if len(ris) == 0:
            return None
        return ris

#modello
    def addAllEdges2(self):

        allEdges = DAO.getAllArchi(self._idMap)
        for e in allEdges:
            self._graph.add_edge( e.o1, e.o2, weight=e.peso)

    def addEdges1(self): #se i nodi sono pochi può convenire
        #doppio ciclo
        for u in self._nodes:
            for v in self._nodes:
                peso = DAO.getPeso(u,v)
                if peso is not None:
                    self._graph.add_edge(u, v, weight=peso)

#-------------------------------------------------------------------------------------------------------------------------------------------------
#TdE-Nyc_hotspot
# GRAFI: semplice, pesato, e NON orientato
# NODI: località l distinte (colonna Location) in cui opera il provider p
query = """select n.Location, avg(n.Latitude) as Latitude, avg(n.Longitude) as Longitude
                    from nyc_wifi_hotspot_locations n
                    where n.Provider = %s
                    group by n.Location """

        cursor.execute(query, (provider,))
        for row in cursor:
            ris.append( Location(**row) )
# ARCHI:  l1 e l2  collegate da un arco se la distanza tra le due località è minore o uguale alla soglia x (utente)
#       -distanza -->  libreria geopy, considerando, media delle latitudini e longitudini degli hotspot
# PESO: distanza tra le due località.