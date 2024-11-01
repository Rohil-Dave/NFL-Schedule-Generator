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

def generate_intra_conference_matchups(standings):
    """
    Generate matchups against another division within the same conference (4 games per team).
    Each team plays all teams in one other division in their conference, with two home and two away games.
    """
    matchups = []
    for conference, divisions in standings.items():
        # Get division names in the conference
        division_keys = list(divisions.keys())
        
        # Rotate divisions to create round-robin pairing for matchups
        num_divisions = len(division_keys)
        for round_num in range(num_divisions - 1):
            for i in range(num_divisions // 2):
                # Pair divisions in a round-robin fashion
                div1 = divisions[division_keys[i]]
                div2 = divisions[division_keys[num_divisions - i - 1]]
                
                # Create matchups between teams in div1 and div2
                for team1 in div1:
                    for team2 in div2:
                        # Randomly assign home and away games
                        if random.choice([True, False]):
                            matchups.append((team1, team2))  # Team1 at home
                        else:
                            matchups.append((team2, team1))  # Team2 at home
                
            # Rotate the list for the next round
            division_keys = [division_keys[0]] + division_keys[1:][::-1]
            
    return matchups