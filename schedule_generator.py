# schedule_generator.py

from nfl_teams import NFL_TEAMS
from schedule_setup import generate_division_matchups

def get_division_games(team_code):
    """Find team's division and return their division opponents."""
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
    """Get list of all team names in a specific division."""
    # Return a list of just the team names from the specified division
    return [team['name'] for team in NFL_TEAMS[conference][division]]

def find_division_matchup(team_conf, team_div, matchups):
    """
    Find the division that matches with the given team's division.
    
    Args:
        team_conf: Conference of the team we're looking up (e.g., 'AFC')
        team_div: Division of the team we're looking up (e.g., 'South')
        matchups: List of (conf1, div1, conf2, div2) tuples from schedule_setup
        
    Returns:
        Tuple of (conference, division) for the matching division
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

def print_all_matchups(intra_matchups, inter_matchups):
    """
    Print all division matchups for testing/verification purposes.
    Shows both intra-conference and inter-conference matchups.
    """
    print("\nTesting - All Division Matchups:")
    
    # Print all intra-conference matchups (divisions within same conference)
    print("\nIntra-Conference Matchups:")
    for conf1, div1, conf2, div2 in intra_matchups:
        print(f"{conf1} {div1} vs {conf2} {div2}")
    
    # Print all inter-conference matchups (AFC vs NFC divisions)    
    print("\nInter-Conference Matchups:")
    for conf1, div1, conf2, div2 in inter_matchups:
        print(f"{conf1} {div1} vs {conf2} {div2}")
    print("\n" + "="*50 + "\n")

def print_team_schedule(team_name, team_code, conf, div, opponents, intra_conf, intra_div, inter_conf, inter_div):
    """
    Print the complete schedule for a team in a formatted way.
    
    Args:
        team_name: Full name of the team
        team_code: Team abbreviation
        conf: Team's conference
        div: Team's division
        opponents: List of division opponents
        intra_conf, intra_div: Conference and division for intra-conference matchups
        inter_conf, inter_div: Conference and division for inter-conference matchups
    """
    # Print team header
    print(f"\nSchedule for {team_name} ({team_code}, an {conf} {div} Team):")
    
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

def main():
    """
    Main function to run the NFL schedule generator.
    Handles the main program flow and user interaction.
    """
    # Generate both types of matchups at program start
    # These remain constant for all team lookups in this session
    intra_matchups = generate_division_matchups('intra')  # Divisions within same conference
    inter_matchups = generate_division_matchups('inter')  # AFC vs NFC divisions
    
    # Display all matchups first for verification
    print_all_matchups(intra_matchups, inter_matchups)
    
    # Start main program loop
    while True:
        # Get team code from user (convert to uppercase for consistency)
        team_code = input("Enter team abbreviation (or 'quit' to exit): ").upper()
        
        # Check for exit condition
        if team_code == 'QUIT':
            break
        
        # Get team information and division opponents
        team_name, conf, div, opponents = get_division_games(team_code)
        
        # Handle case where team code wasn't found
        if not team_name:
            print(f"Team {team_code} not found. Please try again.")
            continue
        
        # Find the divisions this team plays against based on the generated matchups
        intra_conf, intra_div = find_division_matchup(conf, div, intra_matchups)
        inter_conf, inter_div = find_division_matchup(conf, div, inter_matchups)
        
        # Print the complete schedule
        print_team_schedule(
            team_name, team_code, conf, div, opponents,
            intra_conf, intra_div, inter_conf, inter_div
        )

if __name__ == "__main__":
    main()