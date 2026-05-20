import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._choiceTeam = None

    def handleCreaGrafo(self, e):
        year = self._view._ddAnno.value
        if year is None:
            self._view._txtOutSquadre.controls.clear()
            self._view._txtOutSqadre.controls.append(
                ft.Text("Selezionare un anno dal dropdown", color = "red")
            )
            self._view.update_page()
            return
        self._model.buildGraph(year)
        n, m = self._model.getGraphDetails()
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(
            ft.Text(f"Grafo correttamente creato")
        )
        self._view._txt_result.controls.append(
            ft.Text(f"Il grafo contiene {n} nodi e {m} archi")
        )
        self._view.update_page()

    def handleDettagli(self, e):
        if self._choiceTeam is None:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(
                ft.Text("Seleziona una squadra dal menu", color="red")
            )
            self._view.update_page()
            return

        viciniTuples = self._model.getVicini(self._choiceTeam)
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(
            ft.Text(f"Il nodo {self._choiceTeam} ha {len(viciniTuples)} vicini")
        )
        self._view._txt_result.controls.append(
            ft.Text(f"Di seguito una lista ordinata dei vicini:")
        )
        for v in viciniTuples:
            self._view._txt_result.controls.append(
                ft.Text(f"{v[0]} - peso: {v[1]}")
            )

        self._view.update_page()


    def handlePercorso(self, e):
        pass

    def fillDDYears(self):
        years = self._model.getAllYears()

        yearsDD = []
        for y in years:
            yearsDD.append(ft.dropdown.Option(y))

        # Con il metodo map applico la lambda function alla lista years
        # Devo trasformare in list, altrimenti map ritorna un iterable consumabile,
        # cioè dopo che riempio il dropdown diventa vuoto
        yearsDD = list(map(lambda x: ft.dropdown.Option(x), years))

        self._view._ddAnno.options = yearsDD
        self._view.update_page()

    def handleYearSelection(self, e):
        # Questo metodo viene chiamato quando qualcuno ha selezionato un anno dal dropdown,
        # e deve recuperare tutte le squadre che hanno giocato quell'anno e stamparle
        # nel textfield e riempire il dowpdown delle squadre
        year = self._view._ddAnno.value
        if year is None:
            self._view._txtOutSquadre.controls.clear()
            self._view._txtOutSqadre.controls.append(
                ft.Text("Selezionare un anno dal dropdown", color = "red")
            )
            self._view.update_page()
            return

        teams = self._model.getTeamsOfYear(year)

        self._view._txtOutSquadre.controls.clear()
        self._view._txtOutSquadre.controls.append(
            ft.Text(f"Per l'anno {year} sono iscritte al campionato {len(teams)} squadre")
        )

        for t in teams:
            self._view._txtOutSquadre.controls.append(
                ft.Text(t)
            )
            self._view._ddSquadra.options.append(
                ft.dropdown.Option(data = t,
                                   text = t.name,
                                   on_click = self._readDDTeams)
            )
        self._view.update_page()


    def _readDDTeams(self, e):
        if e.control.data is None:
            self._choiceTeam = None

        self._choiceTeam = e.control.data

        print(f"Selezionato il team {self._choiceTeam}")

