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

