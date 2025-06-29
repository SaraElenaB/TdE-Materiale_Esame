def load_interface(self):
    # title
    self._title = ft.Text("Welcome to the TdP Flights Manager", color="green", size=24)
    self._page.controls.append(self._title)

    # ROW with some controls
    self._txtInMin = ft.TextField(label="Numero minimo di compagnie")
    self._btnAnalizzaA = ft.ElevatedButton(text="Analizza aeroporti",
                                           on_click=self._controller.handleAnalisiAeroporti)

    row1 = ft.Row([ft.Container(None, width=250),
                   ft.Container(self._txtInMin, width=250),
                   ft.Container(self._btnAnalizzaA, width=250)],
                  alignment=ft.MainAxisAlignment.CENTER)

    self._ddAeroportoP = ft.Dropdown(label="Aeroporto di Partenza")
    self._btnConnessi = ft.ElevatedButton(text="Aeroporti connessi",
                                          on_click=self._controller.handleConnessiAeroporti,
                                          disabled=True)

    row2 = ft.Row([ft.Container(None, width=250),
                   ft.Container(self._ddAeroportoP, width=250),
                   ft.Container(self._btnConnessi, width=250)],
                  alignment=ft.MainAxisAlignment.CENTER)

    self._ddAeroportoA = ft.Dropdown(label="Aeroporto di Arrivo")
    self._txtInTratte = ft.TextField(label="Numero tratte massimo")
    self._btnCerca = ft.ElevatedButton(text="Cerca itinerario",
                                       on_click=self._controller.handleCercaItinerario)
    self._btnPercorso = ft.ElevatedButton(text="Esiste una tratta?",
                                          on_click=self._controller.handleEsistePercorso)

    row3 = ft.Row([ft.Container(self._ddAeroportoA, width=250),
                   ft.Container(self._txtInTratte, width=250),
                   ft.Container(self._btnCerca, width=250),
                   ft.Container(self._btnPercorso, width=250)],
                  alignment=ft.MainAxisAlignment.CENTER)

    self.txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
    self._page.add(row1, row2, row3, self.txt_result)
    self._page.update()