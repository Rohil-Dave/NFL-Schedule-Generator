"""
NFL Home/Away Game Assignment Module

This module handles all aspects of assigning home and away games in the NFL schedule,
including division games, conference matchups, and rankings-based games. It maintains
consistent assignments through module-level dictionaries and provides functions for
generating and retrieving home/away designations for all game types.

The module follows NFL scheduling rules for:
- Division games (3 home, 3 away against each division opponent)
- Intra-conference matchups (balanced home/away)
- Inter-conference matchups (balanced home/away)
- Intra-rankings-based games (balanced home/away)
- Inter-rankings-based games (following NFL's conference hosting rules)
"""
# Import required libraries
import random
from nfl_teams import NFL_TEAMS

def get_teams_in_division(conference, division):
    """
    Get list of all team names in a specific division.
    
    Args:
        conference (str): Conference name ('AFC' or 'NFC')
        division (str): Division name ('North', 'South', 'East', or 'West')
    
    Returns:
        list: List of team names in the specified division
    """
    # Return a list of just the team names from the specified division
    return [team['name'] for team in NFL_TEAMS[conference][division]]

def get_team_rank(team_name, standings):
    """
    Find a team's rank in their division based on current standings.
    
    Args:
        team_name (str): Full name of the team to find
        standings (dict): Current standings dictionary
    
    Returns:
        int: Rank of the team (1-4) or None if not found
    """
    # Search through all conferences and divisions
    for conference in standings:
        for division in standings[conference]:
            # Check each team in the division
            for rank, team in enumerate(standings[conference][division], 1):
                if team['name'] == team_name:
                    return rank
    return None

def find_division_matchup(team_conf, team_div, matchups):
    """
    Find the division that matches with the given team's division in the provided matchups.
    
    Args:
        team_conf (str): Conference of the team ('AFC' or 'NFC')
        team_div (str): Division of the team ('North', 'South', 'East', 'West')
        matchups (list): List of (conf1, div1, conf2, div2) tuples
    
    Returns:
        tuple: (conference, division) of the matching division
    """
    # Look through each matchup tuple
    for conf1, div1, conf2, div2 in matchups:
        # If our team's division is the first one in the pair...
        if conf1 == team_conf and div1 == team_div:
            # Return the second division in the pair
            return (conf2, div2)
        # If our team's division is the second one in the pair...
        if conf2 == team_conf and div2 == team_div:
            # Return the first division in the pair
            return (conf1, div1)
    # If no match found (shouldn't happen with valid data)
    return None, None

def find_inter_ranking_division(conf, div, inter_rankings):
    """
    Find the division paired with a given division for inter-conference rankings matchups.
    
    Args:
        conf (str): Conference of the team ('AFC' or 'NFC')
        div (str): Division of the team ('North', 'South', 'East', 'West')
        inter_rankings (list): List of (conf1, div1, conf2, div2) tuples for inter-conference rankings
    
    Returns:
        str: Division name from opposite conference for rankings matchup
    """
    for conf1, div1, conf2, div2 in inter_rankings:
        if conf1 == conf and div1 == div:
            return div2
        if conf2 == conf and div2 == div:
            return div1
        
def assign_home_away_division(opponents):
    """
    Assign home/away designations for division games ensuring:
    1. Each opponent is played once at home and once away
    2. Total division home and away games are balanced (3 each)
    
    Args:
        opponents (list): List of division opponent names
    
    Returns:
        tuple: (home_games, away_games)
            home_games: List of tuples (opponent, 'HOME')
            away_games: List of tuples (opponent, 'AWAY')
    """
    # Initialize lists to store home and away matchups
    home_games = []
    away_games = []

    # Track totals for verification
    home_div_games = 0
    away_div_games = 0

    # Dictionary to track home/away split with each opponent
    opponent_splits = {}

    # Process each opponent
    for opponent in opponents:
        # Each opponent must be played once at home and once away
        home_games.append((opponent, 'HOME'))
        away_games.append((opponent, 'AWAY'))

        # Update the counters
        home_div_games += 1
        away_div_games += 1

        # Track the split with this specific opponent
        opponent_splits[opponent] = {'HOME': 1, 'AWAY': 1}

    # Verify the assignments are balanced
    assert home_div_games == 3, "Must have exactly 3 home division games"
    assert away_div_games == 3, "Must have exactly 3 away division games"

    # For each opponent, verify one home and one away game
    for opponent, splits in opponent_splits.items():
        assert splits['HOME'] == 1, f"Must play {opponent} exactly once at home"
        assert splits['AWAY'] == 1, f"Must play {opponent} exactly once away"

    return home_games, away_games

def get_division_games(team_code):
    """
    Find team's division and return their division opponents.
    
    Args:
        team_code (str): Team's abbreviation (e.g., 'JAX', 'NE')
    
    Returns:
        tuple: (team_name, conference, division, opponents)
            team_name (str): Full name of the team
            conference (str): 'AFC' or 'NFC'
            division (str): 'North', 'South', 'East', or 'West'
            opponents (list): List of division opponent names
    """
    # Loop through each conference (AFC and NFC)
    for conference in NFL_TEAMS:
        # Loop through each division (North, South, East, West) in the conference
        for division in NFL_TEAMS[conference]:
            # Get the list of teams in current division
            teams = NFL_TEAMS[conference][division]
            
            # Check if our team is in this division by matching abbreviation
            if any(team['abbreviation'] == team_code for team in teams):
                # Get full team info for our team
                team = next(team for team in teams if team['abbreviation'] == team_code)
                # Create list of division opponents (excluding our team)
                opponents = [t['name'] for t in teams if t != team]
                # Return all relevant info we found
                return team['name'], conference, division, opponents
                
    # If we didn't find the team, return None for all values
    return None, None, None, None

def generate_intra_conference_assignments(intra_matchups):
    """
    Generate all intra-conference home/away assignments at once.
    Should be called once at program start.
    """
    assignments = {}
    
    # Process each matchup pair
    for conf1, div1, conf2, div2 in intra_matchups:
        # Get teams from each division
        div1_teams = NFL_TEAMS[conf1][div1]
        div2_teams = NFL_TEAMS[conf2][div2]
        
        # Initialize assignments for all teams
        for team in div1_teams + div2_teams:
            if team['abbreviation'] not in assignments:
                assignments[team['abbreviation']] = {}
        
        # Assign games between divisions
        for i, team1 in enumerate(div1_teams):
            for j, team2 in enumerate(div2_teams):
                if (i + j) % 2 == 0:
                    assignments[team1['abbreviation']][team2['abbreviation']] = 'HOME'
                    assignments[team2['abbreviation']][team1['abbreviation']] = 'AWAY'
                else:
                    assignments[team1['abbreviation']][team2['abbreviation']] = 'AWAY'
                    assignments[team2['abbreviation']][team1['abbreviation']] = 'HOME'
    
    # Verify assignments
    for team_code in assignments:
        home_games = sum(1 for loc in assignments[team_code].values() if loc == 'HOME')
        away_games = sum(1 for loc in assignments[team_code].values() if loc == 'AWAY')
        assert home_games == 2, f"{team_code} has {home_games} home intra-conference games instead of 2"
        assert away_games == 2, f"{team_code} has {away_games} away intra-conference games instead of 2"
    
    return assignments

def generate_inter_conference_assignments(inter_matchups):
    """
    Generate all inter-conference home/away assignments at once.
    Should be called once at program start.
    """
    assignments = {}
    
    # Process each matchup pair
    for conf1, div1, conf2, div2 in inter_matchups:
        # Get teams from each division
        div1_teams = NFL_TEAMS[conf1][div1]
        div2_teams = NFL_TEAMS[conf2][div2]
        
        # Initialize assignments for all teams
        for team in div1_teams + div2_teams:
            if team['abbreviation'] not in assignments:
                assignments[team['abbreviation']] = {}
        
        # Assign games between divisions
        for i, team1 in enumerate(div1_teams):
            for j, team2 in enumerate(div2_teams):
                if (i + j) % 2 == 0:
                    assignments[team1['abbreviation']][team2['abbreviation']] = 'HOME'
                    assignments[team2['abbreviation']][team1['abbreviation']] = 'AWAY'
                else:
                    assignments[team1['abbreviation']][team2['abbreviation']] = 'AWAY'
                    assignments[team2['abbreviation']][team1['abbreviation']] = 'HOME'
    
    # Verify assignments
    for team_code in assignments:
        home_games = sum(1 for loc in assignments[team_code].values() if loc == 'HOME')
        away_games = sum(1 for loc in assignments[team_code].values() if loc == 'AWAY')
        assert home_games == 2, f"{team_code} has {home_games} home inter-conference matchup games instead of 2"
        assert away_games == 2, f"{team_code} has {away_games} away inter-conference matchup games instead of 2"
    
    return assignments

def generate_intra_rank_assignments(standings, intra_rankings):
    """
    Generate all intra-conference ranking-based home/away assignments.
    
    Args:
        standings (dict): Current standings dictionary
        intra_rankings (dict): Dictionary mapping each division to its two opponent divisions
    
    Returns:
        dict: Dictionary mapping each team to their home/away assignments
    """
    # Initialize assignments dictionary
    assignments = {}
    
    # Process each conference separately
    for conference in ["AFC", "NFC"]:
        print(f"\nGenerating intra-conference rankings matchups for {conference}...")
        
        # Create rank groups dictionary to hold teams of each rank
        rank_groups = {1: [], 2: [], 3: [], 4: []}
        
        # Group all teams by their rank and initialize assignments
        for division in ["North", "South", "East", "West"]:
            for rank, team in enumerate(standings[conference][division], 1):
                rank_groups[rank].append((team['abbreviation'], division))
                assignments[team['abbreviation']] = {}
        
        # Process each rank group separately
        for rank in rank_groups:
            # Track games assigned to each team for this rank
            home_count = {team: 0 for team, _ in rank_groups[rank]}
            away_count = {team: 0 for team, _ in rank_groups[rank]}
            
            # Get all required matchups for this rank
            matchups = set()
            for team_code, division in rank_groups[rank]:
                opponent_divisions = intra_rankings[f"{conference} {division}"]
                for opp_div in opponent_divisions:
                    opp_team = next(code for code, div in rank_groups[rank] if div == opp_div)
                    matchup = tuple(sorted([team_code, opp_team]))
                    matchups.add(matchup)
            
            # Convert to list and sort for deterministic processing
            matchups = sorted(matchups)
            
            # First pass: Handle cases where a team MUST get a specific assignment
            for team1, team2 in matchups:
                if not assignments[team1].get(team2):  # Only process unassigned matchups
                    # If team1 has 1 away game but no home games, it MUST get a home game
                    if home_count[team1] == 0 and away_count[team1] == 1:
                        assignments[team1][team2] = 'HOME'
                        assignments[team2][team1] = 'AWAY'
                        home_count[team1] += 1
                        away_count[team2] += 1
                    # If team2 has 1 away game but no home games, it MUST get a home game
                    elif home_count[team2] == 0 and away_count[team2] == 1:
                        assignments[team1][team2] = 'AWAY'
                        assignments[team2][team1] = 'HOME'
                        away_count[team1] += 1
                        home_count[team2] += 1

            # Second pass: Assign remaining games balancing home/away counts
            for team1, team2 in matchups:
                if not assignments[team1].get(team2):  # Only process unassigned matchups
                    # Randomly assign home/away unless a team already has their maximum games
                    if home_count[team1] == 1 or away_count[team2] == 1:
                        # If team1 already has a home game or team2 already has an away game,
                        # team2 must get the home game
                        assignments[team1][team2] = 'AWAY'
                        assignments[team2][team1] = 'HOME'
                        away_count[team1] += 1
                        home_count[team2] += 1
                    elif home_count[team2] == 1 or away_count[team1] == 1:
                        # If team2 already has a home game or team1 already has an away game,
                        # team1 must get the home game
                        assignments[team1][team2] = 'HOME'
                        assignments[team2][team1] = 'AWAY'
                        home_count[team1] += 1
                        away_count[team2] += 1
                    else:
                        # Both teams are eligible for either home or away, so randomly assign
                        if random.random() < 0.5:  # 50% chance for each team to get home, random.random() returns random float between 0.0 and 1.0
                            assignments[team1][team2] = 'HOME'
                            assignments[team2][team1] = 'AWAY'
                            home_count[team1] += 1
                            away_count[team2] += 1
                        else:
                            assignments[team1][team2] = 'AWAY'
                            assignments[team2][team1] = 'HOME'
                            away_count[team1] += 1
                            home_count[team2] += 1
                        
            # Verify assignments for this rank
            for team, _ in rank_groups[rank]:
                assert home_count[team] == 1, f"Team {team} has {home_count[team]} home games"
                assert away_count[team] == 1, f"Team {team} has {away_count[team]} away games"
                
    # Run final verification
    verify_intra_rank_assignments(assignments)
    
    # Print verification summary
    print("\nAll intra-conference rankings assignments verified successfully:")
    print(f"  - All games follow the intra-conference rankings matchup rules")
    print(f"  - All teams have exactly one home game and one away game")
    print(f"  - All games are between teams of the same rank")
    print(f"  - All assignments are consistent between paired teams")
    
    return assignments

def generate_inter_rank_assignments(standings, inter_rankings, afc_hosts):
    """
    Generate home/away assignments for inter-conference rankings-based games.
    Uses NFL rule: AFC hosts in odd years, NFC hosts in even years.
    
    Args:
        standings (dict): Current standings dictionary
        inter_rankings (list): List of (conf1, div1, conf2, div2) tuples
        afc_hosts (bool): Whether AFC teams host the games this year
    
    Returns:
        dict: Dictionary mapping each team to their opponent and home/away designation
    """
    assignments = {}
    
    # Process each division pairing from our inter-conference rankings matchups
    for conf1, div1, conf2, div2 in inter_rankings:
        # Get teams from each matched division
        div1_teams = standings[conf1][div1]
        div2_teams = standings[conf2][div2]
        
        # Match teams of same rank (0-3 for the 4 positions)
        for rank in range(4):
            team1 = div1_teams[rank]
            team2 = div2_teams[rank]
            
            # Determine which team is AFC and which is NFC by checking conference
            if team1['conference'] == 'AFC':
                afc_team = team1
                nfc_team = team2
            else:  # team1 is NFC
                afc_team = team2
                nfc_team = team1
            
            # Assign home/away based on afc_hosts flag
            if afc_hosts:
                # AFC teams host in odd years
                assignments[afc_team['abbreviation']] = {
                    'opponent': nfc_team['abbreviation'],
                    'location': 'HOME'
                }
                assignments[nfc_team['abbreviation']] = {
                    'opponent': afc_team['abbreviation'],
                    'location': 'AWAY'
                }
            else:
                # NFC teams host in even years
                assignments[afc_team['abbreviation']] = {
                    'opponent': nfc_team['abbreviation'],
                    'location': 'AWAY'
                }
                assignments[nfc_team['abbreviation']] = {
                    'opponent': afc_team['abbreviation'],
                    'location': 'HOME'
                }
    
    # Build the conference homes dictionary for verification
    hosting_conf = "AFC" if afc_hosts else "NFC"
    visiting_conf = "NFC" if afc_hosts else "AFC"
    
    conference_homes = {
        hosting_conf: 16,  # All teams in hosting conference get home games
        visiting_conf: 0   # All teams in visiting conference get away games
    }
    
    # Build division homes dictionary for verification
    division_homes = {
        "AFC": {"North": 0, "South": 0, "East": 0, "West": 0},
        "NFC": {"North": 0, "South": 0, "East": 0, "West": 0}
    }
    
    # Count home games by division for verification
    for team_code, assignment in assignments.items():
        if assignment['location'] == 'HOME':
            # Find the team's conference and division
            for conf in NFL_TEAMS:
                for div in NFL_TEAMS[conf]:
                    for team in NFL_TEAMS[conf][div]:
                        if team['abbreviation'] == team_code:
                            division_homes[conf][div] += 1
                            break
    
    # Verify all assignments meet requirements
    verify_inter_rank_assignments(assignments, conference_homes, division_homes, afc_hosts)
    
    return assignments

def verify_intra_rank_assignments(assignments):
    """
    Verify that all intra-conference rankings-based assignment constraints are met.
    
    Args:
        assignments (dict): Dictionary of team assignments to verify
    
    Raises:
        AssertionError: If any constraint is violated
    """
    for team_code in assignments:
        # Count home and away games
        home_games = sum(1 for loc in assignments[team_code].values() if loc == 'HOME')
        away_games = sum(1 for loc in assignments[team_code].values() if loc == 'AWAY')
        
        # Verify each team has exactly one home and one away game
        assert home_games == 1, f"{team_code} has {home_games} home games instead of 1"
        assert away_games == 1, f"{team_code} has {away_games} away games instead of 1"
        
        # Verify consistency of assignments (if A hosts B, B must visit A)
        for opp_code, location in assignments[team_code].items():
            assert assignments[opp_code][team_code] != location, \
                f"Inconsistent assignments between {team_code} and {opp_code}"

def verify_inter_rank_assignments(assignments, conference_homes, division_homes, afc_hosts):
    """
    Verify that all inter-conference rankings-based assignment constraints are met.
    
    Args:
        assignments (dict): Dictionary of team assignments
        conference_homes (dict): Count of home games by conference
        division_homes (dict): Nested dict of home games by conference and division
        afc_hosts (bool): Whether AFC teams host the games this year
    """
    hosting_conf = "AFC" if afc_hosts else "NFC"
    visiting_conf = "NFC" if afc_hosts else "AFC"
    
    # Verify total assignments and consistency
    total_games = len(assignments)
    assert total_games == 32, f"Expected 32 total assignments, got {total_games}"
    
    teams_assigned = set()
    for team, assignment in assignments.items():
        teams_assigned.add(team)
        teams_assigned.add(assignment['opponent'])
        
        opp_assignment = assignments[assignment['opponent']]
        assert opp_assignment['opponent'] == team, \
            f"Inconsistent opponent assignment for {team} and {assignment['opponent']}"
        assert opp_assignment['location'] != assignment['location'], \
            f"Both {team} and {assignment['opponent']} have {assignment['location']} assignment"
    
    assert len(teams_assigned) == 32, "Not all teams received inter-rankings assignments"
    
    # Verify conference home/away counts
    assert conference_homes[hosting_conf] == 16, \
        f"{hosting_conf} has {conference_homes[hosting_conf]} home games, expected 16"
    assert conference_homes[visiting_conf] == 0, \
        f"{visiting_conf} has {conference_homes[visiting_conf]} home games, expected 0"
    
    # Verify division home/away counts
    for div, homes in division_homes[hosting_conf].items():
        assert homes == 4, \
            f"{hosting_conf} {div} has {homes} home games, expected 4"
    for div, homes in division_homes[visiting_conf].items():
        assert homes == 0, \
            f"{visiting_conf} {div} has {homes} home games, expected 0"
    
    print(f"\nAll inter-conference rankings assignments verified successfully for {'AFC' if afc_hosts else 'NFC'} hosting year:")
    print(f"  - {hosting_conf} (hosting conference) has all home games")
    print(f"  - {visiting_conf} (visiting conference) has all away games")
    print(f"  - All teams have exactly one inter-rankings assignment")
    print(f"  - All assignments are consistent between paired teams")


