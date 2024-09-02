from os import environ

SESSION_CONFIGS = [
    dict(
        name='Pattern',
        display_name="Pattern Experiment",  # Optional, for better readability in the admin interface
        app_sequence=['pattern'],
        num_demo_participants=3,
    ),
]

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00,
    participation_fee=0.00,
    doc=""
)

PARTICIPANT_FIELDS = ['selected_color']
SESSION_FIELDS = []  # Include your custom fields here

# ISO-639 code
LANGUAGE_CODE = 'en'

# Currency settings
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '7056429405491'