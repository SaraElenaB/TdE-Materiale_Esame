#Lab13
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

#-------------------------------------------------------------------------------------------------------------------------------------------------
#Lab12
#a. utente seleziona --> nazione, anno A, tra il 2015 ed il 2018
#grafo semplice, non orientato e pesato
#NODI: tutti retailer presenti nel database
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
        if c1 != c2:  # tutte le possibilità
            peso = DAO.getEdgeWeighted(c1, c2)
            if peso is not None and peso[0] is not None:  # controlla solo quando ha senso: quindi c'è interazione
                self._grafo.add_edge(c1, c2, weight=peso[0])
return self._grafo
