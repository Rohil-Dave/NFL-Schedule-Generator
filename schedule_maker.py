'''
This project is about creating alternative NFL schedules based on an optimized variable of choice.
'''

import random
from data import teams, conferences

def generate_random_standings():
    """Randomize standings within each division and return a dictionary."""
    standings = {}
    for conference, divisions in conferences.items():
        standings[conference] = {}
        for division, division_teams in divisions.items():
            # Shuffle teams to create random standings within the division
            random_standings = random.sample(division_teams, len(division_teams))
            standings[conference][division] = random_standings
    return standings