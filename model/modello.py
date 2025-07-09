
if __name__ == "__main__":
    m = Model()
    mappa = m.getIdMap()
    m.buildGraph(1951)
    print( f"aaaa: {mappa.get(498)} ")
    print( m.getDetailsGraph() )

#https://networkx.org/documentation/stable/reference/algorithms/traversal.html

