
import os


class MaxFlow(object):

    def __init__(self, capacities):
        self.capacities = capacities
        self.N = len(capacities)
        self.parent = [0] * self.N

    def BFS(self, src, dst):
        visited = [False] * self.N

        queue = []

        queue.append(src)
        visited[src] = True

        while queue:

            u = queue.pop(0)
            for i, val in enumerate(self.capacities[u]):
                if visited[i] == False and val > 0:
                    queue.append(i)
                    visited[i] = True
                    self.parent[i] = u
                    if i == dst:
                        return True
        return False

    def findMaxFlow(self, src, dst):
        max_flow = 0

        while self.BFS(src, dst):
            path_flow = float("Inf")
            s = dst
            while(s != src):
                path_flow = min(path_flow, self.capacities[self.parent[s]][s])
                s = self.parent[s]

            max_flow += path_flow

            v = dst
            while(v != src):
                u = self.parent[v]
                self.capacities[u][v] -= path_flow
                self.capacities[v][u] += path_flow
                v = self.parent[v]

        return max_flow

class MinCostMaxFlow(object):
    def __init__(self, capacities, cost) -> None:
        self.capacities = capacities
        self.cost = cost
        self.N = len(self.cost)
        self.infinity = float("inf")
        self.distance = [self.infinity] * (self.N)
        self.parent = [None] * (self.N)

    # cherche s'il existe un chemin de s à t
    def BFS(self, s, t):
        visited = [False] * self.N

        queue = []
        queue.append(s)
        visited[s] = True
        parent = [None] * self.N
        if s == t:
            return True
        while queue:
            u = queue.pop(0)
            for i, capacity in enumerate(self.capacities[u]):
                if visited[i] == False and capacity != 0:
                    queue.append(i)
                    visited[i] = True
                    parent[i] = u
                    if i == t:
                        return True
        return False

    # renvoie le plus court chemin entre src et dst et détecte les cycles négatifs
    def bellmanFord(self, src: int, dst: int):
        self.distance = [self.infinity] * (self.N)
        self.distance[src] = 0
        self.parent = [None for _ in range(self.N)]
        shortest_path = []
        # on fait la distance de tout les sommets avec bellman ford
        for _ in range(self.N - 1):
            for i in range(self.N):
                for j in range(self.N):
                    tmp_dist = self.distance[i] + (self.cost[i][j])
                    if self.distance[j] > tmp_dist and self.capacities[i][j] != 0:
                        self.distance[j] = tmp_dist
                        self.parent[j] = i

        # on regarde s'il y a un cycle négatif
        for i in range(self.N):
            for j in range(self.N):
                tmp_dist = self.distance[i] + (self.cost[i][j])
                if self.distance[j] > tmp_dist and self.capacities[i][j] != 0:
                    print("Cycle négatif, arret de l'algo")
                    return shortest_path

        shortest_path = self.createShortestPath(src, dst)

        return shortest_path

    # créer le shortest path depuis les parents
    def createShortestPath(self, src: int, dst: int):
        shortest_path = []
        s = dst
        while s != src:
            if self.parent[s] is None:
                return False
            shortest_path.insert(0, s)
            s = self.parent[s]
        shortest_path.insert(0, s)
        return shortest_path

    def minCostMaxFlow(self, src: int, dst: int):
        max_flow = 0
        min_cost = 0
        saturated_flow_mc = []
        min_cut = []
        arc_to_link_dot = []
        shortest_path = self.bellmanFord(src, dst)

        # tant que le chemin n'est pas vide et qu'il existe un chemin vers dst
        while shortest_path and shortest_path[-1] == dst:

            path_flow = float("inf")
            # on cherche le flot minimum dans le shortest path
            for s in range(len(shortest_path) - 1):
                u = shortest_path[s]
                v = shortest_path[s+1]
                path_flow = min(path_flow, self.capacities[u][v])

            max_flow += path_flow
            # on met a jour le flot
            for s in range(len(shortest_path) - 1):
                u = shortest_path[s]
                v = shortest_path[s+1]
                # si le flot n'est pas saturé
                if self.capacities[u][v] != 0:
                    min_cost += path_flow * self.cost[u][v]
                    self.capacities[u][v] -= path_flow

                # si le flot est saturé
                if self.capacities[u][v] == 0:
                    # self.capacities[v][u] = 0
                    saturated_flow_mc.append([u, v])

            shortest_path = self.bellmanFord(src, dst)

        for u, v in saturated_flow_mc:
            if self.BFS(src, u) and not self.BFS(src, v):
                min_cut.append([u, v])
            else:
                arc_to_link_dot.append([u, v])

        self.pprintResult(max_flow, min_cost, min_cut)
        try:
            filename = "graph"
            self.createDotFile(f"{filename}.dot", min_cut, src, dst, arc_to_link_dot, max_flow)
            self.generateDotPdf(filename)
        except:
            pass
        return max_flow, min_cost, min_cut

    def pprintResult(self, max_flow: int, min_cost: int, min_cut: list):
        ret = f"Max flow: {max_flow}\nMin cost: {min_cost}\nMin cut "
        for u, v in min_cut:
            ret += f"| ({u} -> {v}) | "
        print(ret)


    def createDotFile(self, file, min_cut: list, src: int, dst: int, arc_to_link_dot, max_flow: int):
        text = """digraph G {
    graph [nodesep="0.3", ranksep="0.3",fontsize=12]
    node [shape=circle,fixedsize=true,width=.3,height=.3,fontsize=12]
    edge [arrowsize=0.6]
"""
        text += f'\ts -> {src}\n'
        for i in range(self.N):
            for j in range(self.N):
                if self.capacities[i][j] != 0:
                    text += f'\t{i} -> {j} [label=<<font color="darkgreen">{self.capacities[i][j]}</font>,<font color="red">{self.cost[i][j]}</font>>]\n'
                elif [i, j] in arc_to_link_dot:
                    text += f'\t{i} -> {j} [color=orange, label=<<font color="orange">saturated</font>>]\n'
        for u, v in min_cut:
            text += f'\t{u} -> {v} [color=red, label=<<font color="red">cut</font>>]\n'

        text += f'\t{dst} -> t \n'
        text += f'\tt -> s [color=blue label=<<font color="blue">max flow = {max_flow}</font>>]\n'
        text += "\ts [color=green]\n\tt [color=blue]\n"
        text += "}"
        with open(file, "w+") as f:
            f.write(text)
        print(f"{file} a été créer...")

    def generateDotPdf(self, filename):
        os.system(f"dot -Tpdf {filename}.dot -o {filename}.pdf")
        print(f"{filename}.pdf a été généré...")

if __name__ == "__main__":

    # start_nodes = [0, 0, 1, 2, 3, 1, 2, 3, 4, 5]
    # end_nodes = [1, 3, 2, 3, 2, 4, 4, 5, 6, 6]
    # capacities = [16, 13, 5, 5, 10, 10, 8, 15, 25, 6]
    # costs = [6, 4, 5, 6, 6, 5, 3, 5, 7, 7]
    # s = 0
    # t = 6

    start_nodes = [ 0, 0,  1, 1,  1,  2, 2,  3, 4]
    end_nodes   = [ 1, 2,  2, 3,  4,  3, 4,  4, 2]
    capacities  = [15, 8, 20, 4, 10, 15, 4, 20, 5]
    costs  = [ 4, 4,  2, 2,  6,  1, 3,  2, 3]
    s = 0
    t = 4

    # start_nodes = [0, 0, 0, 1, 1, 2, 3]
    # end_nodes =   [1, 2, 4, 2, 3, 4, 4]
    # capacities =  [3, 4, 3, 2, 0, 6, 2]
    # costs =       [3, 4, 30, 2, 2, 6, 2]
    # s = 0
    # t = 4

    # start_nodes = [ 0, 0,  1, 1,  1,  2, 2,  3, 4]
    # end_nodes   = [ 1, 2,  2, 3,  4,  3, 4,  4, 2]
    # capacities  = [15, 8, 20, 4, 10, 15, 4, 20, 5]
    # costs  = [ 4, 4,  2, 2,  6,  1, 3,  2, 3]
    # s = 0
    # t = 4

    # start_nodes = [0, 0, 2]
    # end_nodes = [1, 2, 3]
    # capacities = [2, 2, 2]
    # costs = [2, 2, 2]
    # s = 0
    # t = 3

    # start_nodes = [0, 1, 2]
    # end_nodes = [1, 2, 3]
    # capacities = [4, 5, 4]
    # costs = [2, 1, 1]
    # s = 0
    # t = 3

    # start_nodes = [0, 0, 2]
    # end_nodes = [1, 2, 3]
    # capacities = [2, 2, 2]
    # costs = [2, 2, 2]
    # s=0
    # t=3

    # start_nodes = [0, 0, 1, 2, 3, 1, 2, 3, 4, 5]
    # end_nodes   = [1, 3, 2, 3, 2, 4, 4, 5, 6, 6]
    # capacities  = [16,13,5, 5,10,10, 8,15,25, 6]
    # costs       = [6, 4, 5, 6, 6, 5, 3, 5, 7, 7]
    # s = 0
    # t = 6

    # start_nodes = [0, 1, 2, 1]
    # end_nodes = [1, 2, 0, 3]
    # capacities = [2, 2, 2, 2]
    # costs = [1, 1, -3, 1]
    # s = 0
    # t = 3

    # start_nodes = [0, 1, 2, 1]
    # end_nodes = [1, 2, 0, 3]
    # capacities = [2, 2, 2, 2]
    # costs = [1, 1, -2, 1]

    # start_nodes = [ 0, 0,  1, 1,  1,  2, 2,  3, 4]
    # end_nodes   = [ 1, 2,  2, 3,  4,  3, 4,  4, 2]
    # capacities  = [15, 8, 20, 4, 10, 15, 4, 20, 5]
    # costs  = [ 4, 4,  2, 2,  6,  1, 3,  2, 3]
    # s = 0
    # t = 4

    # start_nodes = [0, 1, 2]
    # end_nodes = [1, 2, 3]
    # capacities = [4, 5, 4]
    # costs = [2, 1, 1]
    # s = 0
    # t = 3

    # start_nodes = [0, 0, 0, 1, 1, 2, 3]
    # end_nodes = [1, 2, 4, 2, 3, 4, 4]
    # capacities = [3, 4, 3, 2, 0, 6, 2]
    # costs = [3, 4, 30, 2, 2, 6, 2]
    # s = 0
    # t = 4

    base_nb_nodes = max(max(start_nodes), max(end_nodes)) + 1
    nb_nodes = base_nb_nodes - 1
    if len(start_nodes) > nb_nodes:
        nb_nodes = len(start_nodes)

    graph_capacities = [
        [0 for x in range(base_nb_nodes)] for z in range(base_nb_nodes)
    ]

    graph_costs = [
        [0 for x in range(base_nb_nodes)] for z in range(base_nb_nodes)
    ]

    for i in range(nb_nodes):
        graph_capacities[start_nodes[i]][end_nodes[i]] = capacities[i]
        graph_costs[start_nodes[i]][end_nodes[i]] = costs[i]

    min_cost_max_flow = MinCostMaxFlow(graph_capacities, graph_costs)
    # max_flow, min_cost, min_cut = min_cost_max_flow.minCostMaxFlow(s, t)
    min_cost_max_flow.minCostMaxFlow(s, t)
    # print(f"Max flow {max_flow}, min cost {min_cost}, min cut {min_cut}")
