
#string
def fillDDAnni(self):
    anni = self._model.getAnni()
    for a in anni:
        self._view._ddAnno.options.append(ft.dropdown.Option(a))

    # metodo 2:
    # years= map( lambda x: ft.dropdown.Option(x), anni)
    # ----------------------------------------------------------------------------------------------------------------------------------
#oggetto
def fillDDSquadre(self, anno):
    squadre = self._model.getSquadreAnno(anno)
    for s in squadre:
        self._view._ddSquadra.options.append(ft.dropdown.Option(key=s.teamCode,
                                                                data=s,
                                                                on_click=self._choiceSquadra))

def _choiceSquadra(self, e):
    if e.control.data is None:
        return None
    else:
        self._squadraSelezionata = e.control.data
    print(f" Squadra selezionata chiamata - {self._squadraSelezionata}")


#base di controlli
def handleCreaGrafo(self, e):

        anno = self._view._ddAnno.value
        if anno is None:
            self._view._txtOutSquadre.controls.clear()
            self._view._txtOutSquadre.controls.append( ft.Text("Attenzione, selezionare un anno per continuare", color="red"))
            self._view.update_page()
            return

        self._model.buildGraph(int(anno))
        numNodi, numArchi = self._model.getGrafoDetails()
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append( ft.Text(f"Grafo correttamente creato."))
        self._view._txt_result.controls.append(ft.Text(f"Il grafo è costituito da {numNodi} nodi e {numArchi} archi."))

        self._view._btnDettagli.disabled = False
        self._view._btnPercorso.disabled = False
        self._view.update_page()

#aggiungi archi
#Graph()
edges = DAO.getAllEdges(anno, self._idMapCountries)
        self._graph.add_edges_from(edges)
