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

def generate_pairings_matchups(matchup_type):
    """
    Generate random division matchups for either intra or inter-conference play.
    
    Args:
        matchup_type (str): Either 'intra' or 'inter' to specify matchup type
    
    Returns:
        list: List of tuples containing (conf1, div1, conf2, div2) matchups
    """
    divisions = ["North", "South", "East", "West"]
    matchups = []
    
    if matchup_type == 'intra':
        # Handle intra-conference matchups (AFC vs AFC, NFC vs NFC)
        for conf in ["AFC", "NFC"]:
            # Create a copy of divisions and shuffle them
            div_list = divisions.copy()
            random.shuffle(div_list)
            
            # Pair divisions within the same conference
            matchups.extend([
                (conf, div_list[0], conf, div_list[1]),
                (conf, div_list[2], conf, div_list[3])
            ])
    
    else:  # inter-conference
        # Handle inter-conference matchups (AFC vs NFC)
        afc_divs = divisions.copy()
        nfc_divs = divisions.copy()
        random.shuffle(afc_divs)
        random.shuffle(nfc_divs)
        
        # Create pairs where each AFC division plays an NFC division
        for afc_div, nfc_div in zip(afc_divs, nfc_divs):
            matchups.append(("AFC", afc_div, "NFC", nfc_div))
    
    # Validate matchups
    for conf1, div1, conf2, div2 in matchups:
        if matchup_type == 'intra':
            assert conf1 == conf2, "Intra-conference matchups must be within the same conference"
        else:
            assert conf1 != conf2, "Inter-conference matchups must be between different conferences"
    
    return matchups

def print_pairings_matchups(matchups, matchup_type):
    """
    Print division matchups in a consistent format.
    
    Args:
        matchups (list): List of (conf1, div1, conf2, div2) tuples
        matchup_type (str): Either 'intra' or 'inter' to specify header
    """
    header = "Intra-Conference" if matchup_type == 'intra' else "Inter-Conference"
    print(f"\n{header} Matchups:")
    print("=" * 30)
    
    # Sort matchups by conference to group them together
    sorted_matchups = sorted(matchups, key=lambda x: (x[0], x[1]))
    for conf1, div1, conf2, div2 in sorted_matchups:
        print(f"{conf1} {div1} vs {conf2} {div2}")

def find_other_divisions(conference, paired_division, matchups):
    """
    Find the two divisions in a conference that aren't paired with the given division.
    
    Args:
        conference (str): Conference to search in ('AFC' or 'NFC')
        paired_division (str): Division that's already paired (e.g., 'North')
        matchups (list): List of (conf1, div1, conf2, div2) tuples of intra-conference matchups
    
    Returns:
        list: Two division names that aren't paired with the input division
    """
    all_divisions = ["North", "South", "East", "West"]
    # Find the other division that's paired with our division
    for conf1, div1, conf2, div2 in matchups:
        if conf1 == conference and div1 == paired_division:
            other_paired = div2
            break
        if conf1 == conference and div2 == paired_division:
            other_paired = div1
            break
    
    # Return divisions that aren't our division or its pair
    return [div for div in all_divisions if div != paired_division and div != other_paired]

def generate_rankings_matchups(matchups, matchup_type):
    """
    Generate rankings-based matchups for either intra or inter-conference play.
    
    Args:
        matchups (list): List of division pairings
        matchup_type (str): Either 'intra' or 'inter' to specify matchup type
    
    Returns:
        Union[dict, list]: For intra: Dictionary mapping divisions to opponent divisions
                          For inter: List of (conf1, div1, conf2, div2) tuples
    """
    if matchup_type == 'intra':
        rankings_matchups = {}
        # Process each conference separately
        for conference in ["AFC", "NFC"]:
            # Look at each division in the conference
            for division in ["North", "South", "East", "West"]:
                # Find the two divisions this division will play against
                opponent_divisions = find_other_divisions(conference, division, matchups)
                # Store the matchup information
                rankings_matchups[f"{conference} {division}"] = opponent_divisions
        return rankings_matchups
    
    else:  # inter-conference rankings
        # Get current pairings from matchups
        current_pairs = {}
        for conf1, div1, conf2, div2 in matchups:
            if conf1 == "AFC":
                current_pairs[f"AFC {div1}"] = f"NFC {div2}"
            else:
                current_pairs[f"NFC {div1}"] = f"AFC {div2}"
        
        # Initialize available divisions
        afc_divs = ["North", "South", "East", "West"]
        nfc_divs = ["North", "South", "East", "West"]
        rankings_pairs = []
        used_nfc = set()
        
        # Create rankings-based pairs
        for afc_div in afc_divs:
            # Get the NFC division this AFC division is already paired with
            current_nfc = current_pairs[f"AFC {afc_div}"].split()[1]
            
            # Get available NFC divisions (not current pair and not already used)
            available_nfc = [div for div in nfc_divs 
                           if div != current_nfc and div not in used_nfc]
            
            # Randomly select one of the available NFC divisions
            chosen_nfc = random.choice(available_nfc)
            used_nfc.add(chosen_nfc)
            
            # Add the pairing
            rankings_pairs.append(("AFC", afc_div, "NFC", chosen_nfc))
            
        return rankings_pairs

def print_rankings_matchups(rankings_matchups, matchup_type):
    """
    Print the rankings-based matchups in a formatted way.
    
    Args:
        rankings_matchups: Either dict of division matchups (intra) or list of tuples (inter)
        matchup_type (str): Either 'intra' or 'inter' to specify format
    """
    if matchup_type == 'intra':
        print("\nIntra-Rankings-Based Matchups:")
        for division, opponents in sorted(rankings_matchups.items()):
            conference = division.split()[0]
            print(f"{division} will play same seeds in {conference} {opponents[0]} and {conference} {opponents[1]}")
    else:
        print("\nInter-Rankings-Based Matchups:")
        for conf1, div1, conf2, div2 in sorted(rankings_matchups):
            print(f"{conf1} {div1} will play same seed in {conf2} {div2}")

def main():
    """
    Generate and display random NFL standings and all types of matchups.
    """
    # Generate standings and matchups
    standings = generate_random_standings()
    intra_matchups = generate_pairings_matchups('intra')
    inter_matchups = generate_pairings_matchups('inter')
    intra_rankings = generate_rankings_matchups(intra_matchups, 'intra')
    inter_rankings = generate_rankings_matchups(inter_matchups, 'inter')
    
    # Display results
    print_standings(standings)
    print_pairings_matchups(intra_matchups, 'intra')
    print_pairings_matchups(inter_matchups, 'inter')
    print_rankings_matchups(intra_rankings, 'intra')
    print_rankings_matchups(inter_rankings, 'inter')

if __name__ == "__main__":
    main()