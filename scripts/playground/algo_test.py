import networkx as nx
import matplotlib.pyplot as plt

# Erstelle einen Graphen

G = nx.DiGraph()
pos = {
    1: (0, 0),
    2: (2, 2),
    3: (-2, 2)
}
nx.set_node_attributes(G, pos, 'pos')

# Knoten hinzufügen
G.add_node(1)
G.add_node(2)
G.add_node(3)

# Kanten hinzufügen
G.add_edge(1, 2, color='blue', weight=5)
G.add_edge(2, 3)
G.add_edge(1, 3)
#pos = nx.spring_layout(G)

# Zeichne den Graphen
nx.draw(G, pos, with_labels=True, node_color="grey", node_size=500, font_size=16)
nx.draw_networkx_nodes(G, pos, [1], node_size=500, node_color="lightblue", edgecolors="red")

edge_labels = nx.get_edge_attributes(G, "weight")
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color="red")
print(nx.get_node_attributes(G, 'pos'))
neighbors = list(G.neighbors(1))
print(f"Neighbors of node 1: {neighbors}")
plt.show()
