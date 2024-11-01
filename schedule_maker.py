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

def generate_division_matchups(standings):
    """
    Generate home-and-away matchups within each division (6 games per team).
    Each team plays every other team in its division twice, once at home and once away.
    """
    matchups = []
    for conference, divisions in standings.items():
        for division, teams in divisions.items():
            for i in range(len(teams)):
                for j in range(i + 1, len(teams)):
                    # Each team plays every other team in its division twice (home and away)
                    matchups.append((teams[i], teams[j]))  # Team i hosts Team j
                    matchups.append((teams[j], teams[i]))  # Team j hosts Team i
    return matchups