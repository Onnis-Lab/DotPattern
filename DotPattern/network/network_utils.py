import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random
from network.helper_classes import Scheduler

'''
Contains functions for creating networks and matchmaking algorithms. 
'''

random.seed(734)

def to_ring(n):
    # Calculate polar coordinates for nodes for a ring layout
    theta = np.linspace(0, 2 * np.pi, n, endpoint=False)
    pos = {i: (np.cos(theta[i]), np.sin(theta[i])) for i in range(n)}
    return pos

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

def generate_network_sequences(is_ws, N, k, max_rounds, p_rewire=0.0):
    """Generate game sequences based on network type and parameters."""
    if is_ws:
        # Generate a Watts-Strogatz graph
        G = nx.watts_strogatz_graph(N, k, p_rewire)
    else:
        # Generate a random regular graph
        G = nx.random_regular_graph(k, N)
    
    pos = to_ring(G.number_of_nodes())
    draw(G, pos, save_path='ws_network.pdf' if is_ws else 'random_network.pdf')
    # Use the scheduler to generate sequences for the game
    scheduler = Scheduler(G, max_rounds)
    return scheduler.get_sequences_for_game()