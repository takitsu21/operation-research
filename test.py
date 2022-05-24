class MaxFlow:

    def __init__(self, graph):
        self.graph = graph  # residual graph
        self.row = len(graph)
        self.parent = [0] * self.row

    def BFS(self, s, t):

        # Mark all the vertices as not visited
        visited = [False] * self.row

        # Create a queue for BFS
        queue = []

        # Mark the source node as visited and enqueue it
        queue.append(s)
        visited[s] = True

        # Standard BFS Loop
        while queue:

            # Dequeue a vertex from queue and print it
            u = queue.pop(0)

            # Get all adjacent vertices of the dequeued vertex u
            # If a adjacent has not been visited, then mark it
            # visited and enqueue it
            for ind, val in enumerate(self.graph[u]):
                if visited[ind] == False and val > 0:
                    # If we find a connection to the sink node,
                    # then there is no point in BFS anymore
                    # We just have to set its parent and can return true
                    queue.append(ind)
                    visited[ind] = True
                    self.parent[ind] = u
                    if ind == t:
                        return True

        # We didn't reach sink in BFS starting
        # from source, so return false
        return False

    # Returns the maximum flow from s to t in the given graph

    def findMaxFlow(self, source, sink):

        # This array is filled by BFS and to store path


        max_flow = 0  # There is no flow initially

        # Augment the flow while there is path from source to sink
        while self.BFS(source, sink):

            # Find minimum residual capacity of the edges along the
            # path filled by BFS. Or we can say find the maximum flow
            # through the path found.
            path_flow = float("Inf")
            s = sink
            while(s != source):
                path_flow = min(path_flow, self.graph[self.parent[s]][s])
                s = self.parent[s]

            # Add path flow to overall flow
            max_flow += path_flow

            # update residual capacities of the edges and reverse edges
            # along the path
            v = sink
            while(v != source):
                u = self.parent[v]
                self.graph[u][v] -= path_flow
                self.graph[v][u] += path_flow
                v = self.parent[v]

        return max_flow

class Graph:

    def __init__(self, vertices):
        self.V = vertices # No. of vertices
        self.graph = []
        self.infinity = float("inf")
        self.distance = [self.infinity] * (self.V + 1)
        self.parent = [None for _ in range(self.V)]

    # function to add an edge to graph
    def addEdge(self, u, v, w, capa):
        self.graph.append([u, v, w, capa])

    # utility function used to print the solution
    def printArr(self, dist):
        print("Vertex Distance from Source")
        for i in range(self.V):
            print("{0}\t\t{1}".format(i, dist[i]))

    # The main function that finds shortest distances from src to
    # all other vertices using Bellman-Ford algorithm. The function
    # also detects negative weight cycle
    def BellmanFord(self, src, dst):

        # Step 1: Initialize distances from src to all other vertices
        # as INFINITE
        self.distance[src] = 0


        # Step 2: Relax all edges |V| - 1 times. A simple shortest
        # path from src to any other vertex can have at-most |V| - 1
        # edges
        for _ in range(self.V):

            for u, v, weight, capacity in self.graph:
                tmp_dist = self.distance[u] + weight
                if tmp_dist < self.distance[v]:
                    self.distance[v] = self.distance[u] + weight
                    self.parent[v] = u

        return self.distance, self.parent, self.parent[dst]

    def maxFlow(self, src, dst):
        min_cut = []



class MinCostMaxFlow(object):
    def __init__(self, capacities, cost) -> None:
        self.capacities = capacities
        self.cost = cost
        self.N = len(self.cost)
        self.infinity = float("inf")
        self.distance = [self.infinity] * (self.N + 1)
        self.parent = [0 for _ in range(self.N)]


    def bellmanFord(self, src, dst):
        self.visited = [False] * self.N
        print(self.distance)
        self.distance[src] = 0 # On commence par la source la distance est de 0
        self.visited[src] = True



        while (src != self.N):
            best = self.N
            self.visited[src] = True

            for j in range(self.N):

                # If already self.found
                if (self.visited[j]):
                    continue

                val = (self.distance[src] + self.cost[src][j])

                # If self.dist[k] is > minimum value
                if (self.distance[j] > val):
                    # Update
                    self.distance[j] = val
                    self.parent[j] = src
                if (self.distance[j] > val):

                    # Update
                    self.distance[j] = val
                    self.parent[j] = src

                if (self.distance[j] < self.distance[best]):
                    best = j
            src = best

        return self.parent, self.distance, self.visited[dst]







if __name__ == "__main__":


    start_nodes = [0, 0, 1, 2, 3, 1, 2, 3, 4, 5]
    end_nodes =   [1, 3, 2, 3, 2, 4, 4, 5, 6, 6]
    capacities =  [16,13,5, 5,10,10, 3,15,25, 6]
    costs =       [6, 4, 5, 6, 6, 5, 3, 5, 7, 7]
    graph_capacities = [
        [0 for x in range(len(start_nodes))] for z in range(len(start_nodes))
    ]

    graph_costs = [
        [0 for x in range(len(start_nodes))] for z in range(len(start_nodes))
    ]
    g = Graph(len(start_nodes))
    for i in range(g.V):
        g.addEdge(start_nodes[i], end_nodes[i], costs[i], capacities[i])
        # graph_capacities[start_nodes[i]][end_nodes[i]] = capacities[i]
        # graph_costs[start_nodes[i]][end_nodes[i]] = costs[i]
    # print(graph_costs)
    graph_capacities = [[0, 15, 8, 0, 0],
                  [0, 0, 20, 4, 10],
                  [0, 0, 0, 15, 4],
                  [0, 0, 0, 0, 20],
                  [0, 0, 5, 0, 0]]

    graph_costs = [[0, 4, 4, 0, 0],
            [0, 0, 2, 2, 6],
            [0, 0, 0, 1, 3],
            [0, 0, 0, 0, 2],
            [0, 0, 3, 0, 0]]

    # capacities = [ [ 0, 15, 8, 0, 0 ],
    #     [ 0, 0, 20, 4, 10 ],
    #     [ 0, 0, 0, 15, 4 ],
    #     [ 0, 0, 0, 0, 20 ],
    #     [ 0, 0, 5, 0, 0 ] ]

    # cost = [[0, 4, 4, 0, 0],
    #         [0, 0, 2, 2, 6],
    #         [0, 0, 0, 1, 3],
    #         [0, 0, 0, 0, 2],
    #         [0, 0, 3, 0, 0]]

    # max_flow = MaxFlow(capacities)
    # print(f"Max flow {max_flow.findMaxFlow(0, 4)}")

    # min_cost_max_flow = MinCostMaxFlow([], graph_costs)
    print(f"Max flow {g.BellmanFord(0, 6)}")


