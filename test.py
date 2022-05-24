

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


class MinCostMaxFlow(object):
    def __init__(self, start_nodes, end_nodes, capacities, cost) -> None:
        self.capacities = capacities
        self.cost = cost
        self.start_nodes = start_nodes
        self.end_nodes = end_nodes
        self.N = len(self.cost)
        self.infinity = float("inf")
        self.distance = [self.infinity] * (self.N)
        self.parent = [None] * (self.N)

    def bellmanFord(self, src, dst):
        self.distance = [self.infinity] * (self.N)
        self.distance[src] = 0
        self.parent = [None for _ in range(self.N)]
        self.found = [False for _ in range(self.N)]

        for _ in range(self.N - 1):
            for i in range(self.N):
                tmp_dist = self.distance[self.start_nodes[i]] + (self.cost[i])
                if self.distance[self.end_nodes[i]] > tmp_dist:
                    self.distance[self.end_nodes[i]] = tmp_dist
                    self.parent[self.end_nodes[i]] = self.start_nodes[i]
                    self.found[self.end_nodes[i]] = True

        # print(self.parent)
        s = dst
        while s != src:
            print(f"{self.parent[s]} -> {s}")
            s = self.parent[s]

        print(self.found[self.start_nodes[dst]])
        return self.found[self.end_nodes[dst]]

    def minCost(self, src, dst):
        max_flow = 0

        while self.bellmanFord(src, dst):
            print(self.parent)

            # Find minimum residual capacity of the edges along the
            # path filled by BFS. Or we can say find the maximum flow
            # through the path found.
            path_flow = float("Inf")
            s = dst
            while(s != src):
                # print(self.parent)
                # if self.parent[s] is not None:
                # print(self.parent[s], self.end_nodes[s], self.capacities[self.parent[s]])
                path_flow = min(path_flow, self.capacities[self.parent[s]])
                print(self.capacities[self.parent[s]])
                s = self.parent[s]

            # Add path flow to overall flow
            max_flow += path_flow

            # update residual capacities of the edges and reverse edges
            # along the path
            v = dst
            while(v != src):

                u = self.parent[v]
                self.capacities[u] -= path_flow
                self.capacities[v] += path_flow
                v = self.parent[v]
        return max_flow


if __name__ == "__main__":

    start_nodes = [0, 0, 1, 2, 3, 1, 2, 3, 4, 5]
    end_nodes   = [1, 3, 2, 3, 2, 4, 4, 5, 6, 6]
    capacities  = [16, 13, 5, 5, 10, 10, 3, 15, 25, 6]
    costs       = [6, 4, 5, 6, 6, 5, 3, 5, 7, 7]
    graph_capacities = [
        [0 for x in range(len(start_nodes))] for z in range(len(start_nodes))
    ]

    graph_costs = [
        [0 for x in range(len(start_nodes))] for z in range(len(start_nodes))
    ]
    g = []
    # g = Graph(len(start_nodes))
    for i in range(len(start_nodes)):
        # g.addEdge(start_nodes[i], end_nodes[i], costs[i], capacities[i])
        graph_capacities[start_nodes[i]][end_nodes[i]] = capacities[i]
        graph_costs[start_nodes[i]][end_nodes[i]] = costs[i]
        # g.append(Edge(start_nodes[i], end_nodes[i], capacities[i], costs[i]))
    # print(graph_costs)
    # graph_capacities = [[0, 15, 8, 0, 0],
    #               [0, 0, 20, 4, 10],
    #               [0, 0, 0, 15, 4],
    #               [0, 0, 0, 0, 20],
    #               [0, 0, 5, 0, 0]]

    # graph_costs = [[0, 4, 4, 0, 0],
    #         [0, 0, 2, 2, 6],
    #         [0, 0, 0, 1, 3],
    #         [0, 0, 0, 0, 2],
    #         [0, 0, 3, 0, 0]]

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
    min_cost_max_flow = MinCostMaxFlow(
        start_nodes, end_nodes, capacities, costs)
    print(f"Max flow {min_cost_max_flow.minCost(0, 2)}")
