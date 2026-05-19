import itertools

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        # RICORDA!!! solo Graph per grafi non orientati, DiGraph per grafi orientati
        self._graph = nx.Graph()
        self._teams = []


    def buildGraph(self):
        self._graph.add_nodes_from(self._teams)

        # Aggiungo un arco tra tutte le coppie di nodi del grafo
        for u in self._graph.nodes:
            for v in self._graph.nodes:
                if u!=v:
                    self._graph.add_edge(u,v)

        # Questo metodo prende i team a due a due (tutte le possibile combinazioni)
        #myEdges = itertools.combinations(self._teams, 2)
        #self._graph.add_edges_from(myEdges)


    def getAllYears(self):
        return DAO.getAllYears()

    def getTeamsOfYear(self, year):
        self._teams = DAO.getTeamsOfYear(year)
        return self._teams


    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)