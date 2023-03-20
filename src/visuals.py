import networkx as nx
from .data_structures import Node
from queue import Queue
import matplotlib.pyplot as plt


def draw_graph(root: Node):
    g: nx.Graph = nx.Graph()
    q: Queue[Node] = Queue(maxsize=0)
    q.put(root)
    while not q.empty():
        curr_node = q.get()
        g.add_node(curr_node, color=curr_node.color)
        for n in curr_node.neighbors:
            if n not in g.nodes:
                q.put(n)
            g.add_edge(curr_node, n)

    nx.draw(g, with_labels=True)
    plt.show()
