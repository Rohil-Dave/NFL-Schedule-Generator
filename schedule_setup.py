# Import required libraries
import random
from nfl_teams import NFL_TEAMS  # Import our NFL teams data structure

def generate_random_standings():
    """
    Generate random standings for all NFL divisions.
    Simply shuffles teams within each division to simulate end-of-season standings.
    
    Returns:
        dict: A nested dictionary containing shuffled teams organized by conference and division
              Format: {conference: {division: [team1, team2, team3, team4]}}
    """
    # Initialize empty dictionary with same structure as NFL_TEAMS
    # This will store our randomized standings
    standings = {
        "AFC": {},  # Will contain AFC divisions
        "NFC": {}   # Will contain NFC divisions
    }
    
    # Loop through each conference (AFC and NFC)
    for conference in NFL_TEAMS:
        # Loop through each division in the conference (North, South, East, West)
        for division in NFL_TEAMS[conference]:
            # Create a copy of the teams list to avoid modifying the original NFL_TEAMS data
            teams = NFL_TEAMS[conference][division].copy()
            
            # Randomly shuffle the teams in the division to create standings
            # random.shuffle modifies the list in place
            random.shuffle(teams)
            
            # Store the shuffled teams in our standings dictionary
            standings[conference][division] = teams
    
    return standings

def print_standings(standings):
    """
    Print the standings in a clean, formatted way.
    Shows just the abbreviation for each team, numbered 1-4 for each division.
    
    Args:
        standings (dict): The dictionary containing the randomized standings
    """
    # Loop through each conference (AFC and NFC)
    for conference in standings:
        # Print conference header
        print(f"\n{conference}")
        
        # Loop through each division in the conference
        for division in standings[conference]:
            # Print division header
            print(f"\n{division}:")
            
            # Loop through teams in current division
            # enumerate with start=1 gives us 1-based indexing for standings
            for i, team in enumerate(standings[conference][division], 1):
                # Print team's position and abbreviation
                # e.g., "1. LAR"
                print(f"{i}. {team['abbreviation']}")

def main():
    """
    Main function to execute the standings generation.
    This is the entry point when the script is run directly.
    """
    # Generate random standings for all divisions
    standings = generate_random_standings()
    
    # Display the standings in the console
    print_standings(standings)

# This is a common Python idiom that checks if this file is being run directly
# (as opposed to being imported as a module)
if __name__ == "__main__":
    main()