import networkx as nx
G = nx.Graph()
G.add_node((1,2))
G.add_node((9,3))
G.add_edge((1,2),(9,3))
print(G.nodes)
print(nx.shortest_path_length(G,(1,2),(9,3)))
print(nx.shortest_path_length(G,(1,2),(1,2)))