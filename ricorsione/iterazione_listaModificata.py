
for n in list(nodiDaEscludere):  # oppure set(nodiDaEscludere)
    if n in self._grafo.neighbors(ultimo):
        parziale.append(n)
        nodiDaEscludere.remove(n)