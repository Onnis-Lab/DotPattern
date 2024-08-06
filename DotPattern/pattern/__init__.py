from otree.api import *
from pattern.pattern_utils import get_pattern, compare_patterns
import numpy as np

doc = """
Your app description
"""

class C(BaseConstants):
    NAME_IN_URL = 'pattern'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    PATTERN_SIZE = 10
    N_DOTS = 10


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    reproduced_pattern = models.StringField()  # To store the pattern as a string
    selected_color = models.StringField(
        initial='#000000',
        label="Choose your pattern color:",
        
    )
    # selected_color = models.StringField(initial="#000000", label="Choose your pattern color:")

# FUNCTIONS
def set_random_pattern(player):
    ''' Store the random pattern in a list.'''
    random_pattern = get_pattern(C.PATTERN_SIZE, C.N_DOTS)
    print(random_pattern.tolist())
    player.session.vars['random_pattern'] = random_pattern#.tolist()
    return random_pattern#.tolist()


def store_reproduced_pattern(player):
    # Convert the reproduced pattern string into a matrix
    reproduced_pattern = player.reproduced_pattern.split(',')
    reproduced_pattern = [int(i) for i in reproduced_pattern]
    original_pattern = player.session.vars.get('random_pattern', [])
    reproduced_pattern = np.array(reproduced_pattern).reshape(original_pattern.shape)
    return reproduced_pattern, original_pattern


def get_comparison_results(player):
    original_pattern = player.session.vars.get('random_pattern', [])
    reproduced_pattern, _ = store_reproduced_pattern(player)
    correctness = compare_patterns(original_pattern, reproduced_pattern)
    return correctness, original_pattern, reproduced_pattern


# PAGES
class Instructions(Page):
    form_model = 'player'
    form_fields = ['selected_color']

    # @staticmethod
    # def vars_for_template(player):
    #     return {
    #         'default_color': player.selected_color  # Pass the default or previously selected color
    #     }

class PatternDisplay(Page):
    @staticmethod
    def vars_for_template(player):
        matrix = set_random_pattern(player)
        return {
            'matrix': matrix.tolist(),
            'selected_color': player.selected_color 
        }

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
            'selected_color': player.selected_color
        }

    @staticmethod
    def before_next_page(player, timeout_happened):
        reproduced_pattern = player.reproduced_pattern.split(',')
        # selected_dots = sum(1 for dot in reproduced_pattern if dot == '1')
       

class Results(Page):
    @staticmethod
    def vars_for_template(player):
        correctness, original_pattern, reproduced_pattern = get_comparison_results(player)
        return {
            'accuracy': correctness,
            'original_pattern': original_pattern.tolist(),
            'reproduced_pattern': reproduced_pattern.tolist(),
            'selected_color': player.selected_color
        }


page_sequence = [Instructions, PatternDisplay, Reproduce, Results]