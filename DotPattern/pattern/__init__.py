from otree.api import *
from pattern.pattern_utils import get_pattern, compare_patterns, seed_patterns
from network.network_utils import random_game_sequences, ws_game_sequences
import numpy as np
import json

doc = """
Choose whether the experiment should be run on the random or the watts-strogatz network. 
Depending on that, change the SEQUENCES defined below in the constant (C) class.
"""

###### Change Here Before Releasing #######
DEBUG = False
#############


class C(BaseConstants):
    NAME_IN_URL = 'pattern'
    PLAYERS_PER_GROUP = None
    TEST_MATRIX = np.array([[1, 0, 1], [0, 1, 1], [0, 0, 0]])
    TEST_MATRIX2 = np.array([[0, 1, 1], [0, 0, 1], [0, 1, 0]])
    TEST_MATRIX3 = np.array([[0, 0, 0], [0, 1, 1], [1, 1, 0]])

    
    if DEBUG:
        PATTERN_SIZE = 3 
        N_DOTS = 3
        N_PARTICIPANTS = 3
        PATTERN_DISPLAY_TIME = 3
        REPRODUCE_TIME = 5
        NOODLE_TIME = 1
    else:
        PATTERN_SIZE = 10
        N_DOTS = 12
        N_PARTICIPANTS = 10
        PATTERN_DISPLAY_TIME = 10
        REPRODUCE_TIME = 60
        NOODLE_TIME = 10

    
    INITIAL_PATTERNS = seed_patterns(N_PARTICIPANTS, PATTERN_SIZE, N_DOTS)

    SEQUENCES = random_game_sequences  # or ws_game_sequences
    NUM_ROUNDS = len(SEQUENCES)
    print(SEQUENCES)
    # print(INITIAL_PATTERNS)

class Subsession(BaseSubsession):

    def assign_patterns(self):
        print(f"Assigning patterns for round {self.round_number}")
        if self.round_number == 1:
            # Set initial patterns for all players
            for player in self.get_players():
                initial_pattern = C.INITIAL_PATTERNS[player.id_in_group - 1]
                player.assigned_pattern = json.dumps(initial_pattern.tolist())  # Convert list to JSON string
                player.should_wait = False
                player.rounds_to_wait = 0
                print(f"Round 1: Player {player.id_in_group} assigned pattern {initial_pattern.tolist()}")
        
    def reassign_patterns(self):
        # Handle subsequent rounds
        assert self.round_number > 1
        print(f"Reassigning for round {self.round_number}.\n\n")

        for player in self.get_players():  # players for this round
            print(f"Player {player.id_in_group} is being assigned a new pattern")
            sequence_value = C.SEQUENCES[self.round_number - 2][player.id_in_group - 1]  # Adjust the indexing
            print(f"Round {self.round_number}: Player {player.id_in_group} is getting the pattern from Player {int(sequence_value) + 1}")

            if sequence_value == -1:
                player.should_wait = True
                player.rounds_to_wait += 1
                print(f"Player {player.id_in_group} should wait for {player.rounds_to_wait} rounds")
            elif sequence_value == -2:
                player.should_wait = False
                player.game_over = True
                print(f"Player {player.id_in_group} is done")
            else:
                previous_round = self.round_number - 1
                previous_pattern = None

                # Loop backwards through rounds until a valid pattern is found or we reach the first round
                while previous_round > 0:
                    previous_round_players = self.in_round(previous_round).get_players()
                    print(sequence_value)
                    previous_pattern = previous_round_players[int(sequence_value)].field_maybe_none('reproduced_pattern')

                    if previous_pattern is not None:
                        player.assigned_pattern = previous_pattern
                        print(f"Round {self.round_number}: Player {player.id_in_group} assigned previous pattern {player.assigned_pattern}")
                        break  # Exit the loop once a valid pattern is found
                    else:
                        print(f"Round {self.round_number}: Player {player.id_in_group} has no pattern in round {previous_round}, checking earlier round")
                        previous_round -= 1  # Move to the previous round

                if previous_pattern is None:
                    print(f"Round {self.round_number}: Player {player.id_in_group} could not find any valid pattern in previous rounds")
                    # Handle the case where no valid pattern was found in any previous round

                player.should_wait = False
                player.game_over = False
                player.rounds_to_wait = 0  # Reset if they are playing`

def creating_session(subsession: Subsession):
    if subsession.round_number == 1:
        # for player in subsession.get_players():
        #     player.participant.selected_color = '#000000'
        subsession.assign_patterns()
                    
                
class Group(BaseGroup):
    pass

class Player(BasePlayer):
    reproduced_pattern = models.StringField()  # To store the current reproduced pattern as a string
    assigned_pattern = models.LongStringField()  # To store the current assigned pattern as a JSON string
    selected_color = models.StringField(
        initial='#000000',
        label="Choose your pattern color:",
    )
    should_wait = models.BooleanField(initial=False)
    game_over = models.BooleanField(initial=False)
    rounds_to_wait = models.IntegerField(initial=0)  # Number of rounds to wait

# FUNCTIONS
# In your functions or wherever you manage patterns

def set_random_pattern(player):
    ''' Store the assigned pattern in the session vars for the player '''
    assigned_pattern = player.field_maybe_none('assigned_pattern')
    
    if assigned_pattern is not None:
        assigned_pattern = np.array(eval(assigned_pattern)).reshape((C.PATTERN_SIZE, C.PATTERN_SIZE))  # Convert the stored string back to a NumPy array
    
    return assigned_pattern

def store_reproduced_pattern(player):
    ''' Store the reproduced pattern '''
    assigned_pattern = player.field_maybe_none('assigned_pattern')
    if assigned_pattern is None:
        return None, None
    
    reproduced_pattern = player.reproduced_pattern.split(',')
    reproduced_pattern = [int(i) for i in reproduced_pattern]
    assigned_pattern = np.array(eval(assigned_pattern)).reshape((C.PATTERN_SIZE, C.PATTERN_SIZE))

    reproduced_pattern = np.array(reproduced_pattern).reshape(assigned_pattern.shape)

    return reproduced_pattern, assigned_pattern

def get_comparison_results(player):
    assigned_pattern = np.array(eval(player.assigned_pattern)).reshape((C.PATTERN_SIZE, C.PATTERN_SIZE))

    reproduced_pattern, _ = store_reproduced_pattern(player)
    correctness = compare_patterns(assigned_pattern, reproduced_pattern)
    return correctness, assigned_pattern, reproduced_pattern

# def to_matrix(pattern_string):

#     pattern_mat = []
#     for ch in pattern_string:
#         row = []
#         for _ in range(C.PATTERN_SIZE):
#             row.append(ch)
#         pattern_mat.append(row)

#     return pattern_mat

# PAGES
class Instructions(Page):
    form_model = 'player'
    form_fields = ['selected_color']

    @staticmethod
    def is_displayed(player):
        return player.round_number == 1
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.participant.selected_color = player.selected_color

class WaitforRound(WaitPage):
    @staticmethod
    def is_displayed(player):
        return player.should_wait  # Display the wait page if the player should wait

    @staticmethod
    def get_timeout_seconds(player):
        return player.rounds_to_wait * 70  # 10 display + 60 reproduce

    @staticmethod
    def vars_for_template(player):
        return {
            'message': f"Vennligst vent {player.rounds_to_wait }runde(r) før neste kamp.",
            'wait_time': player.rounds_to_wait * 70
        }

class PatternDisplay(Page):
    timeout_seconds = C.PATTERN_DISPLAY_TIME  # Seconds

    @staticmethod
    def vars_for_template(player):
        matrix = set_random_pattern(player)
        print(f"matrix {matrix}")
        return {
            'matrix': matrix.tolist(),
            'selected_color': player.participant.selected_color,
        }
    
    @staticmethod
    def is_displayed(player: Player):
        return not player.should_wait


class Reproduce(Page):
    form_model = 'player'
    form_fields = ['reproduced_pattern']

    @staticmethod
    def vars_for_template(player):
        size = C.PATTERN_SIZE
        return {
            'pattern_size': range(size),
            'size_value': size,
            'n_dots': C.N_DOTS,
            'selected_color': player.participant.selected_color,
            'reproduce_time': C.REPRODUCE_TIME,
        }

    @staticmethod
    def before_next_page(player, timeout_happened):
        reproduced_pattern = player.reproduced_pattern.split(',')
        # selected_dots = sum(1 for dot in reproduced_pattern if dot == '1')

    @staticmethod
    def is_displayed(player: Player):
        return not player.should_wait
    
class Results(Page):
    @staticmethod
    def vars_for_template(player):
        correctness, assigned_pattern, reproduced_pattern = get_comparison_results(player)
        return {
            'accuracy': correctness,
            'original_pattern': assigned_pattern.tolist(),
            'reproduced_pattern': reproduced_pattern.tolist(),
            'selected_color': player.participant.selected_color,
            "n_dots": C.N_DOTS,
        }

    @staticmethod
    def is_displayed(player: Player):
        return not player.should_wait

class Trial(Page):
    form_model = 'player'
    form_fields = ['reproduced_pattern']

    @staticmethod
    def vars_for_template(player: Player):
        size = 3
        return {
            'matrix': C.TEST_MATRIX.tolist(),
            'flat_matrix': C.TEST_MATRIX.flatten().tolist(),
            'pattern_size': range(size),
            'size_value': size,
            'n_dots': 4,
            'selected_color': player.participant.selected_color
        }
    
    def is_displayed(player: Player):
        return player.round_number == 1
    


class RandomLines(Page):
    timeout_seconds = C.NOODLE_TIME


class WaitForStartGame(WaitPage):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1


class ShuffleWaitPage(WaitPage):
    wait_for_all_groups = True

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number > 1
    
    @staticmethod
    def after_all_players_arrive(subsession: Subsession):
        subsession.reassign_patterns()


class GameOver(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == C.NUM_ROUNDS

    
page_sequence = [
    Instructions,
    Trial,
    WaitForStartGame,
    ShuffleWaitPage,
    WaitforRound,
    PatternDisplay,
    RandomLines, 
    Reproduce,
    Results,
    GameOver,  
]