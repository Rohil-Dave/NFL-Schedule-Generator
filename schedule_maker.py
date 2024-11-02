import random
from data import teams, conferences

def generate_random_standings():
    """Randomize standings within each division and return a dictionary."""
    standings = {}
    for conference, divisions in conferences.items():
        standings[conference] = {}
        for division, division_teams in divisions.items():
            random_standings = random.sample(division_teams, len(division_teams))
            standings[conference][division] = random_standings
    return standings

def generate_division_matchups(standings):
    """
    Generate home-and-away matchups within each division (6 games per team).
    Each team plays twice against every other team in the same division, once at home and once away.
    """
    matchups = []
    for conference, divisions in standings.items():
        for division, teams in divisions.items():
            for i in range(len(teams)):
                for j in range(i + 1, len(teams)):
                    matchups.append((teams[i], teams[j]))
                    matchups.append((teams[j], teams[i]))
    return matchups

def generate_intra_conference_matchups(standings, intra_conf_pairing):
    """
    Generate matchups within the same conference for specific division pairings.
    Each team plays four games against teams from the other division in the same conference.
    Two games at home and two away.
    """
    matchups = []
    for conference, division_pairings in intra_conf_pairing.items():
        for div1, div2 in division_pairings.items():
            division1_teams = standings[conference][div1]
            division2_teams = standings[conference][div2]
            
            # For each team in division1, randomly select 2 home and 2 away opponents
            for team1 in division1_teams:
                away_opponents = random.sample(division2_teams, 2)
                home_opponents = [team2 for team2 in division2_teams if team2 not in away_opponents]
                
                # Add home games
                for team2 in home_opponents:
                    matchups.append((team1, team2))  # Home game for team1
                
                # Add away games
                for team2 in away_opponents:
                    matchups.append((team2, team1))  # Away game for team1
    
    return matchups

def generate_inter_conference_matchups(standings, inter_conf_pairing):
    """Generate matchups between specific paired AFC and NFC divisions."""
    matchups = []
    afc_divisions = standings["AFC"]
    nfc_divisions = standings["NFC"]

    for afc_div, nfc_div in inter_conf_pairing["AFC"].items():
        for team1 in afc_divisions[afc_div]:
            for team2 in nfc_divisions[nfc_div]:
                matchups.append((team1, team2))
    return matchups

def get_matchups(standings):
    """Print matchups for intra-conference and inter-conference games for all divisions."""
    intra_conf_pairing = {"AFC": {}, "NFC": {}}
    inter_conf_pairing = {"AFC": {}, "NFC": {}}

    print("Intra-Conference Matchups:")
    for conference, divisions in standings.items():
        division_keys = list(divisions.keys())
        random.shuffle(division_keys)
        
        for i in range(0, len(division_keys), 2):
            div1, div2 = division_keys[i], division_keys[i + 1]
            intra_conf_pairing[conference][div1] = div2
            intra_conf_pairing[conference][div2] = div1
            print(f"{conference} {div1} vs {conference} {div2}")

    print("\nInter-Conference Matchups:")
    afc_divisions = list(standings["AFC"].keys())
    nfc_divisions = list(standings["NFC"].keys())

    random.shuffle(afc_divisions)
    random.shuffle(nfc_divisions)

    for afc_division, nfc_division in zip(afc_divisions, nfc_divisions):
        inter_conf_pairing["AFC"][afc_division] = nfc_division
        inter_conf_pairing["NFC"][nfc_division] = afc_division
        print(f"AFC {afc_division} vs NFC {nfc_division}")

    return intra_conf_pairing, inter_conf_pairing

def get_team_schedule(standings, division_matchups, intra_conf_matchups, inter_conf_matchups, intra_conf_pairing, inter_conf_pairing):
    """Print the team's schedule with home/away designations."""
    team_shortform = input("Enter the team's short form (e.g., JAX for Jacksonville Jaguars): ").upper()
    
    team = next((t for t in teams if t.shortform == team_shortform), None)
    if not team:
        print(f"Team with short form '{team_shortform}' not found.")
        return

    team_conference = team.conference
    team_division = team.division

    print(f"\nSchedule for {team.full_name} ({team.shortform}, {team_conference} {team_division}):")

    # Division Games
    print(f"\nDivision Opponents (6 games against the {team_conference} {team_division}):")
    division_opponent_games = {}
    
    for matchup in division_matchups:
        if team in matchup:
            opponent = matchup[1] if matchup[0] == team else matchup[0]
            is_home = matchup[0] == team
            
            if opponent not in division_opponent_games:
                division_opponent_games[opponent] = {"home": 0, "away": 0}
            
            if is_home:
                division_opponent_games[opponent]["home"] += 1
            else:
                division_opponent_games[opponent]["away"] += 1

    for opponent, games in division_opponent_games.items():
        print(f"  - {opponent.full_name} ({games['home']} Home, {games['away']} Away)")

    # Intra-Conference Games
    intra_conf_division = intra_conf_pairing[team_conference][team_division]
    print(f"\nIntra-Conference Opponents (4 games against the {team_conference} {intra_conf_division}):")
    intra_conf_opponent_games = {}
    
    for matchup in intra_conf_matchups:
        if team in matchup:
            opponent = matchup[1] if matchup[0] == team else matchup[0]
            is_home = matchup[0] == team
            
            if opponent not in intra_conf_opponent_games:
                intra_conf_opponent_games[opponent] = {"home": 0, "away": 0}
            
            if is_home:
                intra_conf_opponent_games[opponent]["home"] += 1
            else:
                intra_conf_opponent_games[opponent]["away"] += 1

    for opponent, games in intra_conf_opponent_games.items():
        location = "Home" if games["home"] == 1 else "Away"
        print(f"  - {opponent.full_name} ({location})")

    # Inter-Conference Games (unchanged for now)
    inter_conf_conference = "NFC" if team_conference == "AFC" else "AFC"
    inter_conf_division = inter_conf_pairing[team_conference][team_division]
    print(f"\nInter-Conference Opponents (4 games against the {inter_conf_conference} {inter_conf_division}):")
    printed_opponents = set()
    for matchup in inter_conf_matchups:
        if team in matchup:
            opponent = matchup[1] if matchup[0] == team else matchup[0]
            if opponent not in printed_opponents:
                print(f"  - {opponent.full_name}")
                printed_opponents.add(opponent)

# Generate the data and matchups
standings = generate_random_standings()
division_matchups = generate_division_matchups(standings)
intra_conf_pairing, inter_conf_pairing = get_matchups(standings)
intra_conf_matchups = generate_intra_conference_matchups(standings, intra_conf_pairing)
inter_conf_matchups = generate_inter_conference_matchups(standings, inter_conf_pairing)

get_team_schedule(standings, division_matchups, intra_conf_matchups, inter_conf_matchups, intra_conf_pairing, inter_conf_pairing)
