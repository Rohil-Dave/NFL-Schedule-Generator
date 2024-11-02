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
    Displays each conference in a block with divisions aligned horizontally.
    
    Args:
        standings (dict): The dictionary containing the randomized standings
    """
    divisions = ["North", "South", "East", "West"]
    
    # Function to print a single division's standings
    def print_division(conf, div):
        lines = []
        lines.append(f"{div:^20}")  # Center division name in 20 spaces
        lines.append("-" * 20)      # Dividing line
        for i, team in enumerate(standings[conf][div], 1):
            lines.append(f"{i}. {team['abbreviation']:^17}")  # Center team in 17 spaces
        return lines
    
    # Print each conference block
    for conference in ["AFC", "NFC"]:
        print(f"\n{conference}")
        print("=" * 83)  # Separator line for conference
        
        # Get all lines for each division
        division_lines = [print_division(conference, div) for div in divisions]
        
        # Print divisions side by side
        for i in range(len(division_lines[0])):  # All divisions have same number of lines
            line = ""
            for div_lines in division_lines:
                line += div_lines[i] + " | "
            print(line.rstrip(" |"))
        
        print("=" * 83)  # Bottom separator line for conference

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