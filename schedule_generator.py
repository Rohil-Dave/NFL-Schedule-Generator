from nfl_teams import NFL_TEAMS
from schedule_setup import (
    generate_random_standings,
    print_standings,
    generate_pairings_matchups,
    print_pairings_matchups,
    get_ranking_based_opponents
)

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

def print_team_schedule(team_name, team_code, conf, div, opponents, 
                       intra_conf, intra_div, inter_conf, inter_div,
                       rank, rankings_opponents):
    """
    Print the complete schedule for a team in a formatted way.
    
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
        rankings_opponents (list): List of ranking-based opponents
    """

    # Get ordinal form of rank (1st, 2nd, 3rd, 4th)
    rank_ordinal = get_ordinal_suffix(rank)

    # Print team header with rank
    print(f"\nSchedule for {team_name} ({team_code}, an {conf} {div} Team, ranked {rank_ordinal}):")
    
    # Print division games
    print(f"\nDivision Matchups ({conf} {div}):")
    for opponent in opponents:
        print(opponent)
    
    # Print intra-conference games
    print(f"\nIntra-Conference Matchups ({conf} {intra_div}):")
    intra_teams = get_teams_in_division(intra_conf, intra_div)
    for team in intra_teams:
        print(team)
    
    # Print inter-conference games
    print(f"\nInter-Conference Matchups ({inter_conf} {inter_div}):")
    inter_teams = get_teams_in_division(inter_conf, inter_div)
    for team in inter_teams:
        print(team)
        
    # Print rankings-based matchups
    print(f"\nIntra-Rankings-Based Matchups ({rank_ordinal} {conf}):")
    for opponent in rankings_opponents:
        print(opponent)

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
    
    # Display standings and all division pairings first for verification
    print_standings(standings)
    print_pairings_matchups(intra_matchups, 'intra')
    print_pairings_matchups(inter_matchups, 'inter')
    print("\n" + "="*50 + "\n")
    
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
        rankings_opponents = get_ranking_based_opponents(
            conf, div, rank, standings, intra_matchups
        )
        
        # Print the complete schedule
        print_team_schedule(
            team_name, team_code, conf, div, opponents,
            intra_conf, intra_div, inter_conf, inter_div,
            rank, rankings_opponents
        )

if __name__ == "__main__":
    main()