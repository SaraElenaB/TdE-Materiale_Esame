#UNION
#Le query devono avere lo stesso numero di colonne e tipi compatibili (es. non puoi unire una stringa con un numero).
#UNION restituisce solo righe uniche (come DISTINCT).
#Se vuoi includere i duplicati, usa UNION ALL.

query=""" SELECT city FROM customers
            UNION
            SELECT city FROM suppliers"""
            #Questo ti dà l’elenco unificato di città, senza duplicati


query=""" SELECT city FROM customers
            UNION ALL
            SELECT city FROM suppliers """
            #Qui avrai tutte le città, anche quelle ripetute (es. se "Rome" è in entrambe le tabelle).

query=""" select all_airport.id, count(distinct all_airport.airline_id) as numCompagnie
from (select f.ORIGIN_AIRPORT_ID as id, f.AIRLINE_ID
		from flights f 
		group by f.ORIGIN_AIRPORT_ID , f.AIRLINE_ID
		union
		select f.DESTINATION_AIRPORT_ID as id, f.AIRLINE_ID
		from flights f 
		group by f.DESTINATION_AIRPORT_ID , f.AIRLINE_ID) as all_airport
group by all_airport.id
having numCompagnie >= 5
order by all_airport.id"""

#---------------------------------------------------------------------------------------------------------------------------------
# "<" --> per togliere i doppioni
# "COALESCE(t1.numVoli, 0) + COALESCE(t2.numVoli, 0)" -->  funzione che restituisce il primo valore non NULL


#------------------------------------------------------------------------------------------------------------------------------------
# modifico query --> left join vuol dire che inverto la tabella, ho la speculare
        # left join --> sono sicura che l'arco c'è: non è vero ci sono dei NULL
        # tolgo tutto e aggiungo dei filtri: 1. where con < per togliere i doppioni
        #                                    2. COALESCE --> funzione che restituisce il primo elemento che non è null
        # on --> specifica la condizione con cui unire le righe del join
        # or --> quando ho solo andata, il where mi toglie l'andata perciò lo reinserisco

        query = """select t1.ORIGIN_AIRPORT_ID, t1.DESTINATION_AIRPORT_ID, COALESCE(t1.numvoli,0) + coalesce(t2.numvoli,0) as numVoli
                   from (select f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID, count(*) as numVoli
                         from flights f 
                         group by f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID
                         order by f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID) t1
                   left join (select f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID, count(*) as numVoli
                              from flights f 
                              group by f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID
                              order by f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID) t2
                   on t1.origin_airport_id = t2.destination_airport_id
                   and t1.destination_airport_id = t2.origin_airport_id
                   where t1.origin_airport_id < t1.destination_airport_id 
                   or t2.origin_airport_id  is NULL"""