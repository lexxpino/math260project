from math import log
import csv


class Arbitrage:
    def __init__(self, csv_filepath):
        data = []
        curr = []
        with open(csv_filepath) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                row[2] = float(row[2])
                data.append(row)
                if row[0] not in curr:
                    curr.append(row[0])

        self.construct_graph(curr, data)
        self.find_arbitrage()
            
    def construct_graph(self, currencies, rates):
        # currencies = ["USD", "GBP", "YEN", ...]
        # rates = [ ["USD", "GBP", 1.2], ["GBP", "USD", 5/6], ["USD", "YEN", 5.0], ...]
        self.graph = Graph(currencies)
        for rate in rates:
            self.graph.addEdge(rate[0], rate[1], rate[2])
        
        self.graph.modifyEdges()

    def find_arbitrage(self):
        self.graph.bellmanford(self.graph.V[0])

class Graph:
    def __init__(self, vertices):
        self.V = vertices # no. of verts
        self.edges = []
        self.adjacencies = {}
        
    # u, v are vertices, w is weight
    def addEdge(self, u, v, w):
        self.edges.append([u,v,w])
        if u in self.adjacencies:
            self.adjacencies[u].append((v, w))
        else:
            self.adjacencies[u] = []
        
    
    def modifyEdges(self):
        for edge in self.edges:
            edge[2] = (-1) * log(edge[2])

    def bellmanford(self, src):
        dist = {}
        for v in self.V:
            dist[v] = float("Inf")
        dist[src] = 0

        n = len(self.V)
        pre = {}
        for vert in self.V:
            pre[vert] = None
            
        
        for i in range(n-1):
            for v1, v2, w in self.edges:
                
                if dist[v1] != float("Inf") and dist[v1] + w < dist[v2]:
                    dist[v2] = dist[v1] + w
                    pre[v2] = v1
        
        cycles = []
        for v1, v2, w in self.edges:
            
            if dist[v1] != float("Inf") and dist[v1] + w < dist[v2]:
                cycles = [v2, v1]
                # Start from the source and go backwards until you see the source vertex again or any vertex that already exists in print_cycle array
                while pre[v1] not in cycles:
                    cycles.append(pre[v1])
                    v1 = pre[v1]
                cycles.append(pre[v1])
                cycles.reverse()
                print("Arbitrage Opportunity:")
                print(" --> ".join([p for p in cycles[:-1]]))
                print("")
        
        return cycles

if __name__ == "__main__":
    A = Arbitrage('math260/project/data5.csv')
