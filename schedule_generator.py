"""
NFL Schedule Generator Main Module

This module serves as the main program for generating NFL team schedules.
It implements the NFL's scheduling formula to create a complete 17-game schedule
for any team, following the league's scheduling rules introduced in 2021.

Schedule Composition (17 games total):
    - 6 division games (3 home, 3 away)
    - 4 games against another division in same conference
    - 4 games against a division in opposite conference
    - 2 intra-conference games based on prior year's standings
    - 1 inter-conference game based on prior year's standings
        (AFC hosts in odd years, NFC in even years)

Features:
    - Year validation (2021 or later due to 17-game schedule)
    - Proper home/away game distribution
    - Rankings-based matchup generation
    - Balanced schedule generation adhering to NFL rules
    - Detailed schedule display with home/away designations

Main Function:
    main(): Handles user interaction and schedule generation flow

Dependencies:
    nfl_teams.py: NFL teams data structure
    schedule_setup.py: Initial setup and matchup generation functions
    home_away_assignments.py: Home/away game assignment functions

Usage:
    Run this module directly to generate schedules.
    Users will be prompted for:
    1. Year (2021 or later)
    2. Team abbreviation (e.g., 'SF' for San Francisco 49ers)
"""
# import random
from nfl_teams import NFL_TEAMS
from schedule_setup import (
    generate_random_standings,
    print_standings,
    generate_pairings_matchups,
    print_pairings_matchups,
    generate_rankings_matchups,
    print_rankings_matchups,
    get_intra_ranking_based_opponents,
    get_inter_ranking_based_opponent,
)
from home_away_assignments import (
    get_teams_in_division,
    get_team_rank,
    find_division_matchup,
    find_inter_ranking_division,
    assign_home_away_division,
    get_division_games,
    generate_intra_conference_assignments,
    generate_inter_conference_assignments,
    generate_intra_rank_assignments,
    generate_inter_rank_assignments
)

# Module level dictionary to maintain consistency across assignments
INTRA_CONF_ASSIGNMENTS = {}
INTER_CONF_ASSIGNMENTS = {}
INTRA_RANK_ASSIGNMENTS = {}
INTER_RANK_ASSIGNMENTS = {}

def validate_and_get_host_info(year):
    """
    Validate the year input and determine which conference hosts inter-conference rankings-based games.
    The 17th game was added in 2021, and AFC hosts in odd years.
    
    Args:
        year (int): The year to generate the schedule for
        
    Returns:
        tuple: (is_valid, afc_hosts, error_message)
            is_valid (bool): Whether the year is valid
            afc_hosts (bool): Whether AFC hosts in the given year
            error_message (str): Error message if year is invalid, empty string if valid
    """
    # Check if year is 2021 or later
    if year < 2021:
        return False, None, "Invalid year. The 17th game was added in 2021. Please enter 2021 or later."
    
    # Determine if AFC hosts (odd years) or NFC hosts (even years)
    afc_hosts = year % 2 == 1
    host_conf = "AFC" if afc_hosts else "NFC"
    
    return True, afc_hosts, f"For {year}, the {host_conf} will host the inter-rankings-based games"

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
    home_div_games, away_div_games = assign_home_away_division(opponents)

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
    # Get and validate the year first
    while True:
        try:
            year = int(input("\nEnter the year to generate schedule for (2021 or later): "))
            is_valid, afc_hosts, message = validate_and_get_host_info(year)
            if is_valid:
                print(message)
                break
            else:
                print(message)
        except ValueError:
            print("Please enter a valid year (e.g., 2024)")

    # Generate all matchups and standings at program start
    standings = generate_random_standings()
    intra_matchups = generate_pairings_matchups('intra')
    inter_matchups = generate_pairings_matchups('inter')
    intra_rankings = generate_rankings_matchups(intra_matchups, 'intra')
    inter_rankings = generate_rankings_matchups(inter_matchups, 'inter')


    # UN-COMMENT THE FOLLOWING THREE BLOCKS TO PRINT STANDINGS AND MATCHUPS FOR VERIFICATION
    # Display standings and all division pairings first for verification
    print_standings(standings)
    print_pairings_matchups(intra_matchups, 'intra')
    print_pairings_matchups(inter_matchups, 'inter')

    # Display intra-rankings-based matchups for verification
    print_rankings_matchups(intra_rankings, 'intra')

    # Display inter-rankings-based matchups for verification
    print_rankings_matchups(inter_rankings, 'inter')
    print("\n" + "="*50 + "\n")

    # Generate all home/away assignments at start
    global INTRA_CONF_ASSIGNMENTS, INTER_CONF_ASSIGNMENTS, INTRA_RANK_ASSIGNMENTS, INTER_RANK_ASSIGNMENTS
    INTRA_CONF_ASSIGNMENTS = generate_intra_conference_assignments(intra_matchups)
    INTER_CONF_ASSIGNMENTS = generate_inter_conference_assignments(inter_matchups)
    INTRA_RANK_ASSIGNMENTS = generate_intra_rank_assignments(standings, intra_rankings)
    INTER_RANK_ASSIGNMENTS = generate_inter_rank_assignments(standings, inter_rankings, afc_hosts)

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