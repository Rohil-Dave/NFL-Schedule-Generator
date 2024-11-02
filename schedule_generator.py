# schedule_generator.py
from nfl_teams import NFL_TEAMS  # Import our NFL teams data structure

def get_division_games(team_code):
    """Find team's division and return their division opponents."""
    # Loop through each conference (AFC and NFC)
    for conference in NFL_TEAMS:
        # Loop through each division (North, South, East, West) in the conference
        for division in NFL_TEAMS[conference]:
            # Get list of teams in current division
            teams = NFL_TEAMS[conference][division]
            
            # Check if our team is in this division
            # any() returns True if our team code matches any team's abbreviation in this division
            if any(team['abbreviation'] == team_code for team in teams):
                # We found our team's division! Now get the team's full information
                # next() gets the first (and only) team matching our team code
                team = next(team for team in teams if team['abbreviation'] == team_code)
                
                # Create list of opponent names
                # List comprehension: get name of each team that isn't our team
                opponents = [t['name'] for t in teams if t != team]
                
                # Return all the info we need:
                # - Full team name (e.g., "Jacksonville Jaguars")
                # - Conference (e.g., "AFC")
                # - Division (e.g., "South")
                # - List of opponent names in their division
                return team['name'], conference, division, opponents
    
    # If we didn't find the team, return None for all values
    return None, None, None, None

if __name__ == "__main__":
    # Keep running until user quits
    while True:
        # Prompt for team code and convert to uppercase
        team_code = input("\nEnter team abbreviation (or 'quit' to exit): ").upper()
        
        # Check if user wants to quit
        if team_code == 'QUIT':
            break
        
        # Get team information and division opponents
        # This unpacks the four values returned by get_division_games()
        team_name, conf, div, opponents = get_division_games(team_code)
        
        # If team wasn't found (team_name is None)
        if not team_name:
            print(f"Team {team_code} not found. Please try again.")
            # Skip rest of loop and go back to input prompt
            continue
        
        # Print team information and division opponents
        print(f"\nSchedule for {team_name} ({team_code}, an {conf} {div} Team):")
        print("Division Matchups:")
        # Print each opponent on a new line
        for opponent in opponents:
            print(opponent)