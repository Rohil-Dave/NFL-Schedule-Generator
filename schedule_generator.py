import random
from nfl_teams import NFL_TEAMS
from schedule_setup import (
    generate_random_standings,
    print_standings,
    generate_pairings_matchups,
    print_pairings_matchups,
    generate_rankings_matchups,
    print_rankings_matchups
)

# Module level dictionary to maintain consistency across assignments
INTRA_CONF_ASSIGNMENTS = {}
INTER_CONF_ASSIGNMENTS = {}
INTRA_RANK_ASSIGNMENTS = {}
INTER_RANK_ASSIGNMENTS = {}

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

def get_ordinal_suffix(rank):
    """
    Convert a number to its ordinal representation.
    
    Args:
        rank (int): Number to convert (1-4 for NFL standings)
    
    Returns:
        str: Number with appropriate suffix (1st, 2nd, 3rd, 4th)
    """
    if rank == 1:
        return "1st" # st for 1
    elif rank == 2:
        return "2nd" # nd for 2
    elif rank == 3:
        return "3rd" # rd for 3
    else:
        return "4th" # th for 4

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

def get_intra_ranking_based_opponents(team_conf, team_div, team_rank, standings, intra_rankings):
    """
    Get the specific intra-conference opponents for a team based on rankings.
    
    Args:
        team_conf (str): Team's conference ('AFC' or 'NFC')
        team_div (str): Team's division ('North', 'South', 'East', 'West')
        team_rank (int): Team's rank in their division (1-4)
        standings (dict): Current standings dictionary
        intra_rankings (dict): Dictionary of intra-conference rankings matchups
    
    Returns:
        list: Names of the two same-conference opponents based on rankings
    """
    # Get the two divisions this team plays against for rankings
    opponent_divisions = intra_rankings[f"{team_conf} {team_div}"]
    opponents = []
    
    # For each opponent division, find the team at our rank
    for div in opponent_divisions:
        # Get list of teams in that division sorted by standing
        div_teams = standings[team_conf][div]
        # Find team at our rank (subtract 1 because ranks are 1-based but lists are 0-based)
        opponent = div_teams[team_rank - 1]
        opponents.append(opponent['name'])
    
    return opponents

def get_inter_ranking_based_opponent(team_conf, team_div, team_rank, standings, inter_rankings):
    """
    Get the specific inter-conference opponent for a team based on rankings.
    
    Args:
        team_conf (str): Team's conference ('AFC' or 'NFC')
        team_div (str): Team's division ('North', 'South', 'East', 'West')
        team_rank (int): Team's rank in their division (1-4)
        standings (dict): Current standings dictionary
        inter_rankings (list): List of (conf1, div1, conf2, div2) tuples for inter-conference rankings
    
    Returns:
        str: Name of the opposite-conference opponent based on rankings
    """
    # Find the division this team is paired with for inter-conference rankings
    opp_conf = "NFC" if team_conf == "AFC" else "AFC"
    
    # Search through the rankings matchups to find our pairing
    for conf1, div1, conf2, div2 in inter_rankings:
        if conf1 == team_conf and div1 == team_div:
            opp_div = div2
            break
        if conf2 == team_conf and div2 == team_div:
            opp_div = div1
            break
    
    # Get the team at the same rank in the paired division
    opponent = standings[opp_conf][opp_div][team_rank - 1]
    return opponent['name']

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

def assign_home_away_division(team_code, opponents):
    """
    Assign home/away designations for division games ensuring:
    1. Each opponent is played once at home and once away
    2. Total division home and away games are balanced (3 each)
    
    Args:
        team_code (str): Team's abbreviation (e.g., 'JAX', 'NE')
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

def get_intra_conference_games(team_code, intra_conf_teams):
    """
    Get the home/away games for a team from the pre-generated assignments.
    
    Args:
        team_code (str): Team's abbreviation
        intra_conf_teams (list): List of team names from matched division
    
    Returns:
        tuple: (home_games, away_games) lists of tuples
    """
    home_games = []
    away_games = []
    
    # Get opponent codes
    _, team_conf, _, _ = get_division_games(team_code)
    opponent_codes = {}
    for opponent_name in intra_conf_teams:
        for div_teams in NFL_TEAMS[team_conf].values():
            for team in div_teams:
                if team['name'] == opponent_name:
                    opponent_codes[opponent_name] = team['abbreviation']
                    break
    
    # Get assignments from global dictionary
    for opponent_name, opponent_code in opponent_codes.items():
        location = INTRA_CONF_ASSIGNMENTS[team_code][opponent_code]
        if location == 'HOME':
            home_games.append((opponent_name, 'HOME'))
        else:
            away_games.append((opponent_name, 'AWAY'))
    
    return home_games, away_games

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

def get_inter_conference_games(team_code, inter_conf_teams):
    """
    Get the home/away games for a team from the pre-generated assignments.
    
    Args:
        team_code (str): Team's abbreviation
        inter_conf_teams (list): List of team names from matched division in the OPPOSITE conference
    
    Returns:
        tuple: (home_games, away_games) lists of tuples
    """
    home_games = []
    away_games = []
    
    # Get opponent codes
    _, team_conf, _, _ = get_division_games(team_code)
    opp_conf = "NFC" if team_conf == "AFC" else "AFC"
    opponent_codes = {}
    for opponent_name in inter_conf_teams:
        for div_teams in NFL_TEAMS[opp_conf].values():
            for team in div_teams:
                if team['name'] == opponent_name:
                    opponent_codes[opponent_name] = team['abbreviation']
                    break
    
    # Get assignments from global dictionary
    for opponent_name, opponent_code in opponent_codes.items():
        location = INTER_CONF_ASSIGNMENTS[team_code][opponent_code]
        if location == 'HOME':
            home_games.append((opponent_name, 'HOME'))
        else:
            away_games.append((opponent_name, 'AWAY'))
    
    return home_games, away_games

def generate_intra_rank_assignments(standings, intra_rankings):
    """
    Generate all intra-conference ranking-based home/away assignments ensuring balanced
    and randomized assignments. Each team should get exactly 2 games (1 home, 1 away)
    against teams of the same rank from different divisions in their conference.
    
    Args:
        standings (dict): Current standings dictionary
        intra_rankings (dict): Dictionary mapping each division to its two opponent divisions
    
    Returns:
        dict: Dictionary mapping each team to their home/away assignments
    """
    # Initialize tracking dictionaries
    assignments = {}  # Will store final home/away assignments
    processed_pairs = set()  # Track which team pairs we've already processed
    total_games = {}  # Track total games assigned to each team
    home_games = {}  # Track home games assigned to each team
    away_games = {}  # Track away games assigned to each team
    matchups = []  # Will store all matchups we need to process
    
    # Process each conference separately since rankings-based games are intra-conference
    for conference in ["AFC", "NFC"]:
        # Build list of all division-rank combinations
        div_rank_pairs = []
        for division in ["North", "South", "East", "West"]:
            for rank in range(4):  # 0-3 for the 4 positions in each division
                div_rank_pairs.append((division, rank))
        
        # Generate all required matchups
        for division, rank in div_rank_pairs:
            # Get current team's info
            team = standings[conference][division][rank]
            team_code = team['abbreviation']
            
            # Initialize tracking counters for this team if we haven't seen it yet
            if team_code not in total_games:
                total_games[team_code] = 0
                home_games[team_code] = 0
                away_games[team_code] = 0
            
            # Get the two divisions this team needs to play against
            opponent_divisions = intra_rankings[f"{conference} {division}"]
            
            # Process each opponent division
            for opp_div in opponent_divisions:
                # Get the team of same rank from opponent division
                opponent = standings[conference][opp_div][rank]
                opp_code = opponent['abbreviation']
                
                # Initialize tracking counters for opponent if needed
                if opp_code not in total_games:
                    total_games[opp_code] = 0
                    home_games[opp_code] = 0
                    away_games[opp_code] = 0
                
                # Create unique identifier for this pair to avoid duplicates
                pair = tuple(sorted([team_code, opp_code]))
                
                # Only process if we haven't handled this pair yet
                if pair not in processed_pairs:
                    # Randomly order the teams to avoid alphabetical bias
                    if random.random() < 0.5:
                        matchups.append((team_code, opp_code))
                    else:
                        matchups.append((opp_code, team_code))
                    processed_pairs.add(pair)
    
    # Initialize the assignments dictionary for all teams
    for team_code in total_games:
        assignments[team_code] = {}
    
    # Randomly shuffle matchups to ensure random processing order
    random.shuffle(matchups)
    
    # Process each matchup to assign home/away
    for team1, team2 in matchups:
        # Case 1: Neither team has any games yet - randomly assign
        if total_games[team1] == 0 and total_games[team2] == 0:
            if random.random() < 0.5:
                assignments[team1][team2] = 'HOME'
                assignments[team2][team1] = 'AWAY'
                home_games[team1] += 1
                away_games[team2] += 1
            else:
                assignments[team1][team2] = 'AWAY'
                assignments[team2][team1] = 'HOME'
                away_games[team1] += 1
                home_games[team2] += 1
        
        # Case 2: One or both teams have games - must follow balance rules
        else:
            # If team1 needs a home game and team2 can be away
            if home_games[team1] == 0 and away_games[team2] == 0:
                assignments[team1][team2] = 'HOME'
                assignments[team2][team1] = 'AWAY'
                home_games[team1] += 1
                away_games[team2] += 1
            # If team2 needs a home game and team1 can be away
            elif home_games[team2] == 0 and away_games[team1] == 0:
                assignments[team1][team2] = 'AWAY'
                assignments[team2][team1] = 'HOME'
                away_games[team1] += 1
                home_games[team2] += 1
            # If both need home games (should rarely happen due to tracking)
            else:
                # Give home game to team with fewer total games
                if total_games[team1] < total_games[team2]:
                    assignments[team1][team2] = 'HOME'
                    assignments[team2][team1] = 'AWAY'
                    home_games[team1] += 1
                    away_games[team2] += 1
                else:
                    assignments[team1][team2] = 'AWAY'
                    assignments[team2][team1] = 'HOME'
                    away_games[team1] += 1
                    home_games[team2] += 1
        
        # Update total games counter
        total_games[team1] += 1
        total_games[team2] += 1
    
    # Verify assignments
    for team_code in assignments:
        # Verify total number of games
        assert total_games[team_code] == 2, \
            f"{team_code} has {total_games[team_code]} total games instead of 2"
        
        # Verify home/away balance
        assert home_games[team_code] == 1, \
            f"{team_code} has {home_games[team_code]} home games instead of 1"
        assert away_games[team_code] == 1, \
            f"{team_code} has {away_games[team_code]} away games instead of 1"
        
        # Verify consistency of assignments
        for opp_code, location in assignments[team_code].items():
            assert assignments[opp_code][team_code] != location, \
                f"Inconsistent assignments between {team_code} and {opp_code}"
    
    return assignments

def get_intra_rank_games(team_code, intra_rank_opponents):
   """
   Get the home/away games for a team's intra-conference ranking-based games 
   from the pre-generated assignments.
   
   Args:
       team_code (str): Team's abbreviation
       intra_rank_opponents (list): List of team names for ranking-based opponents
   
   Returns:
       tuple: (home_games, away_games) lists of tuples
           home_games (list): List of tuples (opponent_name, 'HOME')
           away_games (list): List of tuples (opponent_name, 'AWAY')
   """
   home_games = []
   away_games = []
   
   # Get opponent codes by searching through NFL_TEAMS
   _, team_conf, _, _ = get_division_games(team_code)
   opponent_codes = {}
   for opponent_name in intra_rank_opponents:
       # Search each division in the conference for this opponent
       for div_teams in NFL_TEAMS[team_conf].values():
           for team in div_teams:
               if team['name'] == opponent_name:
                   opponent_codes[opponent_name] = team['abbreviation']
                   break
   
   # Get assignments from global dictionary
   for opponent_name, opponent_code in opponent_codes.items():
       location = INTRA_RANK_ASSIGNMENTS[team_code][opponent_code]
       if location == 'HOME':
           home_games.append((opponent_name, 'HOME'))
       else:
           away_games.append((opponent_name, 'AWAY'))
   
   # Verify we got exactly one home and one away game
   assert len(home_games) == 1, f"{team_code} has {len(home_games)} home ranking-based games instead of 1"
   assert len(away_games) == 1, f"{team_code} has {len(away_games)} away ranking-based games instead of 1"
   
   return home_games, away_games

def generate_inter_rank_assignments(standings, inter_rankings, existing_assignments=None):
    """
    Generate home/away assignments for inter-conference rankings-based games.
    Ensures balance at conference and division levels while considering existing assignments.
    
    Args:
        standings (dict): Current standings dictionary
        inter_rankings (list): List of (conf1, div1, conf2, div2) tuples for inter-conference rankings
        existing_assignments (dict, optional): Dictionary of existing home/away counts for each team
    
    Returns:
        dict: Dictionary mapping each team to their home/away assignment for this game
    """
    assignments = {}
    
    # Track home games at conference and division level
    conference_homes = {"AFC": 0, "NFC": 0}
    division_homes = {
        "AFC": {"North": 0, "South": 0, "East": 0, "West": 0},
        "NFC": {"North": 0, "South": 0, "East": 0, "West": 0}
    }
    
    # Initialize tracking for already processed teams
    processed_teams = set()
    matchups = []
    
    # First, collect all matchups from the rankings
    for conf1, div1, conf2, div2 in inter_rankings:
        # Get teams from each matched division
        div1_teams = standings[conf1][div1]
        div2_teams = standings[conf2][div2]
        
        # Match teams of same rank
        for rank in range(4):
            team1 = div1_teams[rank]
            team2 = div2_teams[rank]
            team1_code = team1['abbreviation']
            team2_code = team2['abbreviation']
            
            # Create matchup tuple with team info for assignment
            matchup = {
                'team1': {
                    'code': team1_code,
                    'conf': conf1,
                    'div': div1
                },
                'team2': {
                    'code': team2_code,
                    'conf': conf2,
                    'div': div2
                }
            }
            matchups.append(matchup)
    
    # First pass: Assign games where division balance forces the outcome
    for matchup in matchups:
        team1, team2 = matchup['team1'], matchup['team2']
        
        # Skip if either team already processed
        if team1['code'] in processed_teams or team2['code'] in processed_teams:
            continue
            
        # Check if division balance forces assignment
        div1_needs_home = division_homes[team1['conf']][team1['div']] < 2
        div2_needs_home = division_homes[team2['conf']][team2['div']] < 2
        
        # If only one division can still have a home game, assign it
        if div1_needs_home and not div2_needs_home:
            assignments[team1['code']] = {'opponent': team2['code'], 'location': 'HOME'}
            assignments[team2['code']] = {'opponent': team1['code'], 'location': 'AWAY'}
            division_homes[team1['conf']][team1['div']] += 1
            conference_homes[team1['conf']] += 1
            processed_teams.add(team1['code'])
            processed_teams.add(team2['code'])
        elif div2_needs_home and not div1_needs_home:
            assignments[team1['code']] = {'opponent': team2['code'], 'location': 'AWAY'}
            assignments[team2['code']] = {'opponent': team1['code'], 'location': 'HOME'}
            division_homes[team2['conf']][team2['div']] += 1
            conference_homes[team2['conf']] += 1
            processed_teams.add(team1['code'])
            processed_teams.add(team2['code'])
    
    # Second pass: Handle remaining matchups considering conference balance
    for matchup in matchups:
        team1, team2 = matchup['team1'], matchup['team2']
        
        # Skip if already processed
        if team1['code'] in processed_teams or team2['code'] in processed_teams:
            continue
        
        # Check conference and division constraints
        conf1_can_home = conference_homes[team1['conf']] < 8
        conf2_can_home = conference_homes[team2['conf']] < 8
        div1_can_home = division_homes[team1['conf']][team1['div']] < 2
        div2_can_home = division_homes[team2['conf']][team2['div']] < 2
        
        # Determine assignment based on constraints
        if conf1_can_home and div1_can_home and not (conf2_can_home and div2_can_home):
            # Give home game to team1
            assignments[team1['code']] = {'opponent': team2['code'], 'location': 'HOME'}
            assignments[team2['code']] = {'opponent': team1['code'], 'location': 'AWAY'}
            division_homes[team1['conf']][team1['div']] += 1
            conference_homes[team1['conf']] += 1
        else:
            # Give home game to team2
            assignments[team1['code']] = {'opponent': team2['code'], 'location': 'AWAY'}
            assignments[team2['code']] = {'opponent': team1['code'], 'location': 'HOME'}
            division_homes[team2['conf']][team2['div']] += 1
            conference_homes[team2['conf']] += 1
        
        processed_teams.add(team1['code'])
        processed_teams.add(team2['code'])
    
    # Verify assignments
    verify_inter_rank_assignments(assignments, conference_homes, division_homes)
    
    return assignments

def verify_inter_rank_assignments(assignments, conference_homes, division_homes):
    """
    Verify that all inter-conference rankings-based assignment constraints are met.
    
    Args:
        assignments (dict): Dictionary of team assignments
        conference_homes (dict): Count of home games by conference
        division_homes (dict): Nested dict of home games by conference and division
    
    Raises:
        AssertionError: If any constraint is violated
    """
    # Count total assignments
    total_games = len(assignments)
    assert total_games == 32, f"Expected 32 total assignments, got {total_games}"
    
    # Verify each team has exactly one assignment
    teams_assigned = set()
    for team, assignment in assignments.items():
        teams_assigned.add(team)
        teams_assigned.add(assignment['opponent'])
        
        # Verify home/away consistency
        opp_assignment = assignments[assignment['opponent']]
        assert opp_assignment['opponent'] == team, \
            f"Inconsistent opponent assignment for {team} and {assignment['opponent']}"
        assert opp_assignment['location'] != assignment['location'], \
            f"Both {team} and {assignment['opponent']} have {assignment['location']} assignment"
    
    assert len(teams_assigned) == 32, "Not all teams received inter-rankings assignments"
    
    # Verify conference balance
    for conf, homes in conference_homes.items():
        assert homes == 8, f"{conf} has {homes} home games instead of 8 for inter-rankings game"
    
    # Verify division balance
    for conf in division_homes:
        for div, homes in division_homes[conf].items():
            assert homes == 2, f"{conf} {div} has {homes} home games instead of 2 for inter-rankings game"
    
    print("All inter-rankings assignments verified successfully:")
    print(f"  - Each conference has exactly 8 home games")
    print(f"  - Each division has exactly 2 home games")
    print(f"  - All teams have exactly one inter-rankings assignment")
    print(f"  - All assignments are consistent between paired teams")

def get_inter_rank_games(team_code, inter_rank_opponent):
    """
    Get the home/away designation for a team's inter-conference ranking-based game.
    
    Args:
        team_code (str): Team's abbreviation
        inter_rank_opponent (str): Name of the opponent team
    
    Returns:
        tuple: (home_game, away_game) where one will be empty and the other will contain
               the (opponent_name, location) tuple
    """
    home_games = []
    away_games = []
    
    # Get opponent code by searching through NFL_TEAMS
    _, team_conf, _, _ = get_division_games(team_code)
    opp_conf = "NFC" if team_conf == "AFC" else "AFC"
    opponent_code = None
    
    # Find opponent's abbreviation
    for div_teams in NFL_TEAMS[opp_conf].values():
        for team in div_teams:
            if team['name'] == inter_rank_opponent:
                opponent_code = team['abbreviation']
                break
        if opponent_code:
            break
    
    # Get assignment from global dictionary
    location = INTER_RANK_ASSIGNMENTS[team_code]['location']
    if location == 'HOME':
        home_games.append((inter_rank_opponent, 'HOME'))
    else:
        away_games.append((inter_rank_opponent, 'AWAY'))
    
    return home_games, away_games

def print_team_schedule(team_name, team_code, conf, div, opponents, 
                       intra_conf, intra_div, inter_conf, inter_div,
                       rank, intra_rank_opponents, intra_rank_divisions, 
                       inter_rank_opponent, inter_rank_div):
    """
    Print the complete schedule for a team in a formatted way.
    Now includes home/away designations for division games, intra-conference matchup games,
    inter-conference matchup games, and intra-rankings-based games.
    
    Args:
        team_name (str): Full name of the team
        team_code (str): Team abbreviation
        conf (str): Team's conference
        div (str): Team's division
        opponents (list): List of division opponents
        intra_conf (str): Conference for intra-conference matchups
        intra_div (str): Division for intra-conference matchups
        inter_conf (str): Conference for inter-conference matchups
        inter_div (str): Division for inter-conference matchups
        rank (int): Team's rank in their division
        intra_rank_opponents (list): List of same-conference ranking-based opponents
        intra_rank_divisions (list): List of divisions for intra-conference ranking matchups
        inter_rank_opponent (str): Opposite-conference ranking-based opponent
        inter_rank_div (str): Division for inter-conference ranking matchup
    """
    # Get ordinal form of rank (1st, 2nd, 3rd, 4th)
    rank_ordinal = get_ordinal_suffix(rank)
    
    # Print team header with rank
    print(f"\nSchedule for {team_name} ({team_code}, an {conf} {div} Team, ranked {rank_ordinal}):")

    # Get actual home/away assignments for division games
    home_div_games, away_div_games = assign_home_away_division(team_code, opponents)

    # Print division games
    print(f"\nDivision Matchups ({conf} {div}):")
    for opponent in opponents:
        # Count actual home and away games for this opponent
        home_count = sum(1 for game in home_div_games if game[0] == opponent)
        away_count = sum(1 for game in away_div_games if game[0] == opponent)
        print(f"{opponent} ({home_count} HOME, {away_count} AWAY)")
    
    # Get intra-conference games with home/away designations
    intra_conf_teams = get_teams_in_division(intra_conf, intra_div)
    home_intra_games, away_intra_games = get_intra_conference_games(team_code, intra_conf_teams)

    # Print intra-conference games
    print(f"\nIntra-Conference Matchups ({conf} {intra_div}):")
    for opponent, location in home_intra_games + away_intra_games:
        print(f"{opponent} ({location})")
    
    # Get inter-conference games with home/away designations
    inter_conf_teams = get_teams_in_division(inter_conf, inter_div)
    home_inter_games, away_inter_games = get_inter_conference_games(team_code, inter_conf_teams)

    # Print inter-conference games
    print(f"\nInter-Conference Matchups ({inter_conf} {inter_div}):")
    for opponent, location in home_inter_games + away_inter_games:
        print(f"{opponent} ({location})")
    
    # Get intra-conference ranking-based games with home/away designations
    home_intra_rank_game, away_intra_rank_game = get_intra_rank_games(team_code, intra_rank_opponents)
    
    # Print intra-conference rankings-based matchups
    print(f"\nIntra-Rankings-Based Matchups ({rank_ordinal} {conf} {intra_rank_divisions[0]} and {rank_ordinal} {conf} {intra_rank_divisions[1]}):")
    for opponent, location in home_intra_rank_game + away_intra_rank_game:
        print(f"{opponent} ({location})")

    # Get inter-conference ranking-based game with home/away designations
    home_inter_rank_game, away_inter_rank_game = get_inter_rank_games(team_code, inter_rank_opponent)

    # Print inter-conference rankings-based matchup
    print(f"\nInter-Rankings-Based Matchup ({rank_ordinal} {inter_conf} {inter_rank_div}):")
    for opponent, location in home_inter_rank_game + away_inter_rank_game:
        print(f"{opponent} ({location})")

    # Print summary
    total_home = len(home_div_games) + len(home_intra_games) + len(home_inter_games) + \
                 len(home_intra_rank_game) + len(home_inter_rank_game)
    total_away = len(away_div_games) + len(away_intra_games) + len(away_inter_games) + \
                 len(away_intra_rank_game) + len(away_inter_rank_game)
    print(f"\nTotal Games: {total_home + total_away} ({total_home} HOME, {total_away} AWAY)")

    print("=" * 30)

def main():
    """
    Main function to run the NFL schedule generator.
    Handles the main program flow and user interaction.
    """
    # Generate all matchups and standings at program start
    standings = generate_random_standings()
    intra_matchups = generate_pairings_matchups('intra')
    inter_matchups = generate_pairings_matchups('inter')
    intra_rankings = generate_rankings_matchups(intra_matchups, 'intra')
    inter_rankings = generate_rankings_matchups(inter_matchups, 'inter')
    
    # Display standings and all division pairings first for verification
    print_standings(standings)
    print_pairings_matchups(intra_matchups, 'intra')
    print_pairings_matchups(inter_matchups, 'inter')

    # Display inter-rankings-based matchups for verification
    print_rankings_matchups(inter_rankings, 'inter')
    print("\n" + "="*50 + "\n")

    # Generate all home/away assignments at start
    global INTRA_CONF_ASSIGNMENTS, INTER_CONF_ASSIGNMENTS, INTRA_RANK_ASSIGNMENTS, INTER_RANK_ASSIGNMENTS
    INTRA_CONF_ASSIGNMENTS = generate_intra_conference_assignments(intra_matchups)
    INTER_CONF_ASSIGNMENTS = generate_inter_conference_assignments(inter_matchups)
    INTRA_RANK_ASSIGNMENTS = generate_intra_rank_assignments(standings, intra_rankings)
    INTER_RANK_ASSIGNMENTS = generate_inter_rank_assignments(standings, inter_rankings)

    # Print verification message after generating assignments
    print("\nVerifying assignments...")
    print(f"Intra-conference assignments created for {len(INTRA_CONF_ASSIGNMENTS)} teams")
    print(f"Inter-conference assignments created for {len(INTER_CONF_ASSIGNMENTS)} teams")
    print(f"Intra-rankings assignments created for {len(INTRA_RANK_ASSIGNMENTS)} teams")
    print(f"Inter-rankings assignments created for {len(INTER_RANK_ASSIGNMENTS)} teams")
    
    while True:
        team_code = input("\nEnter team abbreviation (or 'quit' to exit): ").upper()
        
        if team_code == 'QUIT':
            break
        
        # Get team information and division opponents
        team_name, conf, div, opponents = get_division_games(team_code)
        
        if not team_name:
            print(f"Team {team_code} not found. Please try again.")
            continue
        
        # Find the divisions this team plays against
        intra_conf, intra_div = find_division_matchup(conf, div, intra_matchups)
        inter_conf, inter_div = find_division_matchup(conf, div, inter_matchups)
        
        # Get team's rank and rankings-based opponents
        rank = get_team_rank(team_name, standings)
        
        # Get intra-conference rankings-based opponents and their divisions
        intra_rank_divisions = intra_rankings[f"{conf} {div}"]
        intra_rank_opponents = get_intra_ranking_based_opponents(
            conf, div, rank, standings, intra_rankings
        )
        
        # Get inter-conference rankings-based opponent and division
        inter_rank_div = find_inter_ranking_division(conf, div, inter_rankings)
        inter_rank_opponent = get_inter_ranking_based_opponent(
            conf, div, rank, standings, inter_rankings
        )
        
        # Print the complete schedule for the requested team
        print_team_schedule(
            team_name, team_code, conf, div, opponents,
            intra_conf, intra_div, inter_conf, inter_div,
            rank, intra_rank_opponents, intra_rank_divisions,
            inter_rank_opponent, inter_rank_div
        )

if __name__ == "__main__":
    main()