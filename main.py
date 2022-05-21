
# Python3 program to implement
# the above approach
from sys import maxsize
from typing import List

INF = float("inf")

class MinCostMaxFlow(object):
    def __init__(self, capacities, cost) -> None:
        # Stores the self.found edges

        # Stores the number of nodes

        # Stores the capacity
        # of each edge
        self.capacities = capacities

        # Stores the self.cost per
        # unit self.flow of each edge
        self.cost = cost

        # Stores the distance from each node
        # and picked edges for each node
        self.N = len(self.capacities)
        self.found = [False for _ in range(self.N)]
        self.flow = [[0 for _ in range(self.N)]
                for _ in range(self.N)]
        self.dist = [INF for _ in range(self.N + 1)]
        self.dad = [0 for _ in range(self.N)]
        self.pi = [0 for _ in range(self.N)]



    # Function to check if it is possible to
    # have a self.flow from the src to sink
    def search(self, src: int, sink: int) -> bool:

        # Initialise self.found[] to false
        self.found = [False for _ in range(self.N)]

        # Initialise the self.dist[] to INF
        self.dist = [INF for _ in range(self.N + 1)]

        # Distance from the source node
        self.dist[src] = 0

        # Iterate until src reaches N
        while (src != self.N):
            best = self.N
            self.found[src] = True

            for k in range(self.N):

                # If already self.found
                if (self.found[k]):
                    continue

                # Evaluate while self.flow
                # is still in supply
                if (self.flow[k][src] != 0):

                    # Obtain the total value
                    val = (self.dist[src] + self.pi[src] -
                            self.pi[k] - self.cost[k][src])

                    # If self.dist[k] is > minimum value
                    if (self.dist[k] > val):

                        # Update
                        self.dist[k] = val
                        self.dad[k] = src

                if (self.flow[src][k] < self.capacities[src][k]):
                    val = (self.dist[src] + self.pi[src] -
                            self.pi[k] + self.cost[src][k])

                    # If self.dist[k] is > minimum value
                    if (self.dist[k] > val):

                        # Update
                        self.dist[k] = val
                        self.dad[k] = src

                if (self.dist[k] < self.dist[best]):
                    best = k

            # Update src to best for
            # next iteration
            src = best

        for k in range(self.N):
            self.pi[k] = min(self.pi[k] + self.dist[k], INF)

        # Return the value obtained at sink
        return self.found[sink]

    # Function to obtain the maximum Flow
    def getMaxFlow(self, src: int, sink: int) -> List[int]:

        # global self.capacities, self.cost, self.found, self.dist, self.pi, N, self.flow, self.dad



        totflow = 0
        totcost = 0

        # If a path exist from src to sink
        while (self.search(src, sink)):

            # Set the default amount
            amt = INF
            x = sink

            while x != src:
                amt = min(
                    amt, self.flow[x][self.dad[x]] if
                    (self.flow[x][self.dad[x]] != 0) else
                    self.capacities[self.dad[x]][x] - self.flow[self.dad[x]][x])
                x = self.dad[x]

            x = sink

            while x != src:
                if (self.flow[x][self.dad[x]] != 0):
                    self.flow[x][self.dad[x]] -= amt
                    totcost -= amt * self.cost[x][self.dad[x]]

                else:
                    self.flow[self.dad[x]][x] += amt
                    totcost += amt * self.cost[self.dad[x]][x]

                x = self.dad[x]

            totflow += amt


        # Return pair total self.cost and sink
        return [totflow, totcost]

# Driver Code
if __name__ == "__main__":

    s = 0
    t = 4

    capacities = [ [ 0, 15, 8, 0, 0 ],
            [ 0, 0, 20, 4, 10 ],
            [ 0, 0, 0, 15, 4 ],
            [ 0, 0, 0, 0, 20 ],
            [ 0, 0, 5, 0, 0 ] ]

    cost = [ [ 0, 4, 4, 0, 0 ],
            [ 0, 0, 2, 2, 6 ],
            [ 0, 0, 0, 1, 3 ],
            [ 0, 0, 0, 0, 2 ],
            [ 0, 0, 3, 0, 0 ] ]

    minCostMaxFlow = MinCostMaxFlow(capacities, cost)

    flow, cost = minCostMaxFlow.getMaxFlow(s, t)

    print("Max flow : {}, Min cost : {}".format(flow, cost))