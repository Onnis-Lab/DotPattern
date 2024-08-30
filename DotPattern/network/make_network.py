import random

'''
Contains functions for creating networks and matchmaking algorithms. 
'''

random.seed(4567)

# NETWORK
N_NEIGHBORS = 4
N_NODES = 16

# GAME
MAX_ROUNDS = 10


# WATTS-STROGATZ NETWORK
P_REWIRE = 0.0


random_path = "random_network.pdf"
ws_path = "ws_network.pdf"

# Create the graphs
random_G = nx.random_regular_graph(N_NEIGHBORS, N_NODES)
ws_G = nx.watts_strogatz_graph(N_NODES, N_NEIGHBORS, P_REWIRE)
pos = to_ring(N_NODES)

random_scheduler = Scheduler(random_G, MAX_ROUNDS)
random_game_sequences = random_scheduler.get_sequences_for_game()

ws_scheduler = Scheduler(ws_G, MAX_ROUNDS)
ws_game_sequences = ws_scheduler.get_sequences_for_game()


if __name__ == '__main__':
    
    # Draw the graphs (optional)
    # draw(random_G, pos, save_path=random_path)
    # draw(ws_G, pos, save_path=ws_path)

    # draw(random_G, pos)
    # draw(ws_G, pos)
    
    # Generate random patterns

    # print(random_patterns)

    
    # paths = random_scheduler.get_paths()

    print(random_game_sequences)
    print(ws_game_sequences)
    # for path in paths:
    #     # print(f"random \n\n\n\n")
    #     print(f"Pattern {int(path[0])} goes through {path}")
        # print(f"Number of nodes {len(set(path))}.")

    # ws_paths = ws_scheduler.get_paths()
    # print(ws_game_sequences) 
    # print(f"ws \n\n\n\n")
    # for path in ws_paths:
    #     print(f"Pattern {int(path[0])} goes through {path}")
        # print(f"Number of nodes {len(set(path))}.")
