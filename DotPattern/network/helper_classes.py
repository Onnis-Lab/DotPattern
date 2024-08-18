import random
import numpy as np

# GAME CODE

NO_AVAILABLE_NEIGHBOUR = -1
END_OF_GAME = -2

class Scheduler:

    def __init__(self, graph, n_rounds):
        """
        args:
            graph: a networkx graph object,
            n_rounds: int, the number of rounds a pattern must travel in the graph.
        """
        self.graph = graph 
        self.n_rounds = n_rounds

        self.sequences = np.empty((0, graph.number_of_nodes()))
        self.sequences = np.vstack([self.sequences, np.arange(graph.number_of_nodes())]) # round 0, everyone gets an initial pattern

    def find_an_available_neighbour(self, node, round_participants):
        """Randomly chooses an available neighbour to pass the pattern onto, if available.
        args:
            node: index of the node in the network;
            round_participants: set, the nodes that have already been selected by other nodes.
        return:
            neighbour_nodes: int, the index of the neighbouring node selected;
            """
        
        neighbours = list(self.graph.neighbors(node))
        random.shuffle(neighbours)
        for neighbour in neighbours:
            if neighbour not in round_participants:
                return neighbour

        return None

    def _find_last_non_negative(self, i, round):
        assert round >= 0 
        if round == 0:
            return self.sequences[round, i]
        new_node = self.sequences[round - 1, i]
        if new_node >= 0:
            return new_node
        else:
            return self._find_last_non_negative(i, round - 1)
            
    def count_paths(self, path):
        """Count the number of games the pattern has been through"""
        return sum(1 for i in path if i >= 0)

    def get_sequence_for_round(self, round):
        """
        Append the next player that would get the pattern to the sequence"""
        end_game_counter = 0
        sequence = np.zeros(self.graph.number_of_nodes(), dtype=int) # for a round
        round_participants = set()
        if round > 0:
            for i, node in enumerate(self.sequences[round - 1]):
                if self.count_paths(self.sequences[:, i]) == self.n_rounds:
                    sequence[i] = END_OF_GAME
                    end_game_counter += 1
                    continue
                if node == NO_AVAILABLE_NEIGHBOUR:
                    node = self._find_last_non_negative(i, round - 2)
                neighbour = self.find_an_available_neighbour(node, round_participants)
                if neighbour is not None:
                    round_participants.add(neighbour)
                    sequence[i] = neighbour
                else:
                    sequence[i] = NO_AVAILABLE_NEIGHBOUR # no available neighbour
            if end_game_counter < self.graph.number_of_nodes(): 
                self.sequences = np.vstack([self.sequences, sequence])

        return end_game_counter == self.graph.number_of_nodes()
    
    def get_sequences_for_game(self):
        round = 1
        is_end_game = False
        while not is_end_game:
            # print(f"round: {round}")
            is_end_game = self.get_sequence_for_round(round)
            round += 1
        
        return self.sequences

    def get_paths(self):
        return self.sequences.T



class PatternManager:
    
    def __init__(self, pattern_dict):

        """
        args: patterns: dictionary,  key: int, node index, value: 2d-array, initial pattern
        """


            



