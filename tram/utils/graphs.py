import networkx as nx
import graphviz

class Graph(nx.Graph):
    def __init__(self, start=None):
        super().__init__(start)

    def neighbors(self, n):
        return list(self[n])

    def vertices(self):
        return self.nodes()

    def add_vertex(self,a):
        self.add_node(a)

    def remove_vertex(self, vertex):
        self.remove_node(vertex)

    def get_vertex_value(self, v):
        return self.nodes[v]['value']

    def set_vertex_value(self, v, x):
        self.nodes[v]['value'] = x

class WeightedGraph(Graph):
    def __init__(self, start=None):
        super().__init__(start)

    def set_weight(self, a, b, w):
        self[a][b]['weight'] = w

    def get_weight(self, a, b): 
        return self[a][b]['weight']
    
def dijkstra(graph, source, cost=lambda u, v: 1):
    def costs2attributes(G, cost, attr="weight"):
        for a, b in G.edges():
            G[a][b][attr] = cost(a, b)
    costs2attributes(graph, cost)
    return nx.shortest_path(graph, source, weight="weight")

def visualize(graph, view="view", name="mygraph", nodecolors=None):
    gv_graph = graphviz.Graph()
    for a in graph.vertices():
        if nodecolors and str(a) in nodecolors:
            gv_graph.node(str(a), fillcolor=nodecolors[str(a)], style="filled")
        else:
            gv_graph.node(str(a))
    for a, b in graph.edges():
        gv_graph.edge(str(a), str(b))
    if view:
        gv_graph.render(view=True)
    else:
        gv_graph.render() 

def view_shortest(G, source, target, cost=lambda u, v: 1):
    path = dijkstra(G, source, cost)[target]
    colormap = {str(v): "orange" for v in path}
    visualize(G, view="view", nodecolors=colormap)

def demo():
    G = Graph([(1, 2), (1, 3), (1, 4), (3, 4), (3, 5), (3, 6), (3, 7), (6, 7)])
    view_shortest(G, 2, 6)
