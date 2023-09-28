from otree.api import *
from pattern.pattern_utils import get_pattern, compare_patterns

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'pattern'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    PATTERN_SIZE = 10


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


# PAGES
class PatternDisplay(Page):
    
    form_model = 'player'
    # form_fields = ['pattern']

    def vars_for_template(self):
        random_pattern = get_pattern(C.PATTERN_SIZE)
        return {
            'matrix': random_pattern.tolist(),
        }

    # timeout stuff

class Reproduce(Page):
    form_model = 'player'
    # form_fields = ['pattern']

    def vars_for_template(self):
        return 
    



class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [PatternDisplay, Reproduce, ResultsWaitPage, Results]
