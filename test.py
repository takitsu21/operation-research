

import enum
from tracemalloc import start


class MaxFlow:

    def __init__(self, capacities):
        self.graph = capacities
        self.row = len(capacities)
        self.parent = [0] * self.row

    def BFS(self, s, t):
        visited = [False] * self.row

        queue = []

        queue.append(s)
        visited[s] = True

        while queue:

            u = queue.pop(0)
            for ind, val in enumerate(self.graph[u]):
                if visited[ind] == False and val > 0:
                    queue.append(ind)
                    visited[ind] = True
                    self.parent[ind] = u
                    if ind == t:
                        return True
        return False


    def findMaxFlow(self, source, sink):
        max_flow = 0

        while self.BFS(source, sink):
            path_flow = float("Inf")
            s = sink
            while(s != source):
                path_flow = min(path_flow, self.graph[self.parent[s]][s])
                s = self.parent[s]

            max_flow += path_flow

            v = sink
            while(v != source):
                u = self.parent[v]
                self.graph[u][v] -= path_flow
                self.graph[v][u] += path_flow
                v = self.parent[v]

        return max_flow


class Edge:
    def __init__(self, u, v, cost, capacity) -> None:
        self.u = u
        self.v = v
        self.cost = cost
        self.capacity = capacity
        self.distance = float("inf")




    def __repr__(self) -> str:
        return f"<u: {self.u} v: {self.v} cost: {self.cost} capacity: {self.capacity}>"


class MinCostMaxFlow(object):
    def __init__(self, start_nodes: list, end_nodes: list, capacities, cost, g: list[Edge]) -> None:
        self.capacities = capacities
        self.cost = cost
        self.start_nodes = start_nodes
        self.end_nodes = end_nodes
        self.N = len(self.cost)
        self.infinity = float("inf")
        self.distance = [self.infinity] * (self.N)
        self.parent = [None] * (self.N)
        self.g = g
        # print(self.g)

    def BFS(self, s, t):
        visited = [False] * self.N

        queue = []

        queue.append(s)
        visited[s] = True
        parent = [None] * self.N
        while queue:

            u = queue.pop(0)
            for ind, val in enumerate(self.g[u]):
                if visited[ind] == False and val != -1:
                    queue.append(ind)
                    visited[ind] = True
                    if ind == t:
                        return True
        return False



    def bellmanFord(self, src, dst):
        self.distance = [self.infinity] * (self.N)
        self.distance[src] = 0
        self.parent = [None for _ in range(self.N)]

        for _ in range(self.N - 1):
            for i in range(self.N):
                u = self.start_nodes[i]
                v = self.end_nodes[i]
                tmp_dist = self.distance[u] + (self.cost[u][v])
                if self.distance[v] > tmp_dist and self.capacities[u][v] != 0:
                    self.distance[v] = tmp_dist
                    self.parent[v] = u

                # u = self.g[i].u
                # for j in range(self.N):
                #     u_edge: Edge = self.g[i][j]
                #     v_edge: Edge = self.g[j][i]
                #     print(u_edge, v_edge)
                #     tmp_dist = u_edge.distance + (u_edge.cost)
                #     if v_edge.distance > tmp_dist and u_edge.capacity != 0:
                #         self.g[i].distance = tmp_dist
                #         self.parent[v_edge.v] = u_edge.u
                #     print(self.parent)
        shortest_path = []
        s = dst
        while s != src:
            print(s)
            if self.parent[s] is None:
                return False
            shortest_path.insert(0, s)
            s = self.parent[s]
        shortest_path.insert(0, s)
        print(shortest_path)
        return shortest_path

    def minCost(self, src, dst):
        max_flow = 0
        min_cost = 0
        min_cut = []
        shortest_path = self.bellmanFord(src, dst)
        print(shortest_path)
        while shortest_path and shortest_path[-1] == dst:

            path_flow = float("inf")
            for s in range(len(shortest_path) - 1):
                u = shortest_path[s]
                v = shortest_path[s+1]
                path_flow = min(path_flow, self.capacities[u][v])

            max_flow += path_flow
            for s in range(len(shortest_path) - 1):
                u = shortest_path[s]
                v = shortest_path[s+1]
                if self.capacities[u][v] != 0:
                    min_cost += path_flow * self.cost[u][v]
                    print(f"u = {u}, v = {v}")
                    self.capacities[u][v] -= path_flow

                else:
                    self.capacities[v][u] = 0
                    self.start_nodes.remove(u)
                    self.end_nodes.remove(v)
                    self.N -= 1
                if self.capacities[u][v] == 0:
                    min_cut.append([u, v])
            shortest_path = self.bellmanFord(src, dst)
        mc2 = []
        print(min_cut)
        for u, v in min_cut:
            if not self.BFS(src, u) and self.BFS(src, v):
                mc2.append([u, v])
        # print(self.g)
        return max_flow, min_cost, mc2


if __name__ == "__main__":

    # start_nodes = [0, 0, 1, 2, 3, 1, 2, 3, 4, 5]
    # end_nodes   = [1, 3, 2, 3, 2, 4, 4, 5, 6, 6]
    # capacities  = [16,13,5, 5,10,10, 8,15,25, 6]
    # costs       = [6, 4, 5, 6, 6, 5, 3, 5, 7, 7]

    # s = 0
    # t = 6
    # start_nodes = [ 0, 0,  1, 1,  1,  2, 2,  3, 4]
    # end_nodes   = [ 1, 2,  2, 3,  4,  3, 4,  4, 2]
    # capacities  = [15, 8, 20, 4, 10, 15, 4, 20, 5]
    # costs  = [ 4, 4,  2, 2,  6,  1, 3,  2, 3]

    start_nodes = [0, 0, 0, 1, 1, 2, 3]
    end_nodes =   [1, 2, 4, 2, 3, 4, 4]
    capacities =  [3, 4, 3, 2, 0, 6, 2]
    costs =       [3, 4, 30, 2, 2, 6, 2]
    s = 0
    t = 4

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

    max_node = len(start_nodes)

    graph_capacities = [
        [0 for x in range(max_node)] for z in range(max_node)
    ]

    graph_costs = [
        [0 for x in range(max_node)] for z in range(max_node)
    ]
    g = [[Edge(0, 0, 0, 0) for x in range(max_node)] for z in range(max_node)]

    print(graph_costs)

    for i in range(len(start_nodes)):
        graph_capacities[start_nodes[i]][end_nodes[i]] = capacities[i]
        graph_costs[start_nodes[i]][end_nodes[i]] = costs[i]
        # g[start_nodes[i]][end_nodes[i]] = end_nodes[i]
        # g.append(Edge(start_nodes[i], end_nodes[i], costs[i], capacities[i]))
    # for i in range(len(start_nodes)):
    #     if len(end_nodes) <= end_nodes[i]:
    #         g[start_nodes[i]][i] = Edge(start_nodes[i], end_nodes[i], costs[i], capacities[i])
    #     else:
    #         g[start_nodes[i]][end_nodes[i]] = Edge(start_nodes[i], end_nodes[i], costs[i], capacities[i])
    # print(g)
    print(graph_capacities)
    min_cost_max_flow = MinCostMaxFlow(
        start_nodes, end_nodes, graph_capacities, graph_costs, g)
    print(f"Max flow {min_cost_max_flow.minCost(s, t)}")
