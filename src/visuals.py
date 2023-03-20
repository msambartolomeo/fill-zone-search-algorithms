import networkx as nx
from .data_structures import Node
from queue import Queue
from typing import Set
import matplotlib.pyplot as plt


def draw_graph(root: Node):
    q: Queue[Node] = Queue(maxsize=0)
    g: nx.Graph = nx.Graph()
    q.put(root)
    visited: Set[Node] = {root}

    while not q.empty():
        curr_node = q.get()
        g.add_node(curr_node, color=curr_node.color)
        for n in curr_node.neighbors:
            if n not in visited:
                q.put(n)
                visited.add(n)
            g.add_edge(curr_node, n)

    nx.draw(g, with_labels=True)
    plt.show()
