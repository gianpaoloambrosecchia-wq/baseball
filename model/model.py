import copy
import itertools

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        # RICORDA!!! solo Graph per grafi non orientati, DiGraph per grafi orientati
        self._graph = nx.Graph()

        self._idMapTeams = {}
        self._bestPath = []
        self._bestObjectVal = 0

    def getPath(self, v0):
        self._bestPath = []
        self._bestObjectVal = 0
        parziale = [v0]

        for v in self._graph.neighbors(v0):
            parziale.append(v)
            self._ricorsione(parziale)
            parziale.pop()


    def _ricorsione(self, parziale):
        # 1) Condizione di ottimalità: verifico se parziale è migliore del best
        if self._score(parziale) > self._bestObjectVal:
            self._bestPath = copy.deepcopy(parziale)
            self._bestObjectVal = self._score(parziale)
        # 2) Condizione di terminazione: verifico se posso continuare

        # 3) Ricorsione
        for v in self._graph.neighbors(parziale[-1]):
            # Peso dell'arco corrente
            pesoE = self._graph[parziale[-1]][v]["weight"]
            # Considero il peso dell'arco precedente, cioè l'arco che unisce il penultimo elemento di parziale [-2]
            # e l'ultimo elemento di parziale [-1]
            if self._graph[parziale[-2]][parziale[-1]]["weight"] > pesoE and v not in parziale:
                parziale.append(v)
                self._ricorsione(parziale)
                parziale.pop()

    def _score(self, parziale):
        score = 0
        # Accedo così agli archi perche so che in parziale ogni elemento è collegato al successivo con un arco
        for i in range(len(parziale)-1):
            score += self._graph[parziale[i]][parziale[i+1]]["weight"]
        return score



    def buildGraph(self, year):
        self._graph.clear()

        self._graph.add_nodes_from(self._teams)

        # Aggiungo un arco tra tutte le coppie di nodi del grafo
        for u in self._graph.nodes:
            for v in self._graph.nodes:
                if u!=v:
                    self._graph.add_edge(u,v)

        # Questo metodo prende i team a due a due (tutte le possibile combinazioni)
        #myEdges = itertools.combinations(self._teams, 2)
        #self._graph.add_edges_from(myEdges)

        self._idMapTeams = {t.ID : t for t in self._graph.nodes}


        # AGGIUNGO I PESI AGLI ARCHI
        mapSalary = DAO.getSalariesOfTeam(year, self._idMapTeams)
        # Cioè considero tutti gli archi del grafo e per ogni arco inserisco il peso dell'arco come somma dei salari
        # dei due team
        for e in self._graph.edges:
            # e[0] è il primo vertice dell'arco (primo team)
            salario1 = mapSalary[e[0]]
            # e[1] è il secondo vertice dell'arco (secondo team)
            salario2 = mapSalary[e[1]]
            peso = salario1 + salario2
            self._graph[e[0]][e[1]]["weight"] = peso


    def getVicini(self, source):
        vicini = self._graph.neighbors(source)
        # viciniTuples è una lista di tuple con primo elemento il vicino e seconod elemento
        # il peso dell'arco da source a vicino (e posso così facilmente ordinarla)
        viciniTuples = []
        for v in vicini:
            viciniTuples.append((v, self._graph[source][v]["weight"]))

        viciniTuples.sort(key = lambda x: x[1], reverse = True)
        return viciniTuples


    def getAllYears(self):
        return DAO.getAllYears()

    def getTeamsOfYear(self, year):
        self._teams = DAO.getTeamsOfYear(year)
        return self._teams


    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)
