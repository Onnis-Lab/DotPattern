import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random
from network.helper_classes import Scheduler 
# from helper_classes import Scheduler 


def to_ring(n):
    # Calculate polar coordinates for nodes for a ring layout
    theta = np.linspace(0, 2*np.pi, n, endpoint=False)
    pos = {i: (np.cos(theta[i]), np.sin(theta[i])) for i in range(n)}
    return pos

# Draw the graph
def draw(G, pos=None, with_labels=True, node_color='skyblue', save_path=None):
    if pos:
        nx.draw(G, pos, with_labels=with_labels, node_size=100, node_color=node_color)
    else:
        nx.draw(G, with_labels=with_labels, node_size=20, node_shape='8')

    plt.gca().set_aspect('equal', adjustable='box')
    if save_path:
        plt.savefig(save_path)
        plt.close()
    else:
        plt.show()

def watts_strogatz(N=12, k=4, p=0.4):
    # Generate the graph
    G = nx.watts_strogatz_graph(N, k, p)
    pos = to_ring(N)
    # Draw the graph using the polar coordinates
    draw(G, pos)



