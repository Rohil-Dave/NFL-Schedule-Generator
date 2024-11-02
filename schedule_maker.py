# """
# This project is about creating alternative NFL schedules based on an optimized variable of choice.
# """

# import random
# from data import teams, conferences

# def generate_random_standings():
#     """Randomize standings within each division and return a dictionary."""
#     standings = {}
#     for conference, divisions in conferences.items():
#         standings[conference] = {}
#         for division, division_teams in divisions.items():
#             # Shuffle teams to create random standings within the division
#             random_standings = random.sample(division_teams, len(division_teams))
#             standings[conference][division] = random_standings
#     return standings

# def generate_division_matchups(standings):
#     """
#     Generate home-and-away matchups within each division (6 games per team).
#     Each team plays every other team in its division twice, once at home and once away.
#     """
#     matchups = []
#     for conference, divisions in standings.items():
#         for division, teams in divisions.items():
#             for i in range(len(teams)):
#                 for j in range(i + 1, len(teams)):
#                     # Each team plays every other team in its division twice (home and away)
#                     matchups.append((teams[i], teams[j]))  # Team i hosts Team j
#                     matchups.append((teams[j], teams[i]))  # Team j hosts Team i
#     return matchups

# def generate_intra_conference_matchups(standings, intra_conf_pairing):
#     """
#     Generate matchups within the same conference for specific division pairings (4 games per team).
#     Each team plays all teams in its specifically paired intra-conference division without duplication.
#     """
#     matchups = []
    
#     for conference, division_pairings in intra_conf_pairing.items():
#         for div1, div2 in division_pairings.items():
#             division1_teams = standings[conference][div1]
#             division2_teams = standings[conference][div2]
            
#             # Pair each team in div1 with each team in div2 without duplication
#             for team1 in division1_teams:
#                 for team2 in division2_teams:
#                     matchups.append((team1, team2))

#     return matchups

# def generate_inter_conference_matchups(standings, inter_conf_pairing):
#     """
#     Generate matchups between specific paired AFC and NFC divisions.
#     Each team in an AFC division plays each team in its specifically paired NFC division.
#     """
#     matchups = []
#     afc_divisions = standings["AFC"]
#     nfc_divisions = standings["NFC"]

#     # Pair each AFC division with its assigned NFC division based on inter_conf_pairing
#     for afc_div, nfc_div in inter_conf_pairing["AFC"].items():
#         for team1 in afc_divisions[afc_div]:
#             for team2 in nfc_divisions[nfc_div]:
#                 matchups.append((team1, team2))  # No home/away designation

#     return matchups

# def get_matchups(standings):
#     """
#     Print matchups for intra-conference and inter-conference games for all divisions.
#     Returns dictionaries of intra- and inter-conference pairings.
#     """
#     intra_conf_pairing = {"AFC": {}, "NFC": {}}
#     inter_conf_pairing = {"AFC": {}, "NFC": {}}

#     # 1. Intra-Conference Matchups
#     print("Intra-Conference Matchups:")
#     for conference, divisions in standings.items():
#         division_keys = list(divisions.keys())
#         random.shuffle(division_keys)
        
#         for i in range(0, len(division_keys), 2):
#             div1, div2 = division_keys[i], division_keys[i + 1]
#             intra_conf_pairing[conference][div1] = div2
#             intra_conf_pairing[conference][div2] = div1
#             print(f"{conference} {div1} vs {conference} {div2}")

#     # 2. Inter-Conference Matchups
#     print("\nInter-Conference Matchups:")
#     afc_divisions = list(standings["AFC"].keys())
#     nfc_divisions = list(standings["NFC"].keys())

#     random.shuffle(afc_divisions)
#     random.shuffle(nfc_divisions)

#     for afc_division, nfc_division in zip(afc_divisions, nfc_divisions):
#         inter_conf_pairing["AFC"][afc_division] = nfc_division
#         inter_conf_pairing["NFC"][nfc_division] = afc_division
#         print(f"AFC {afc_division} vs NFC {nfc_division}")

#     return intra_conf_pairing, inter_conf_pairing

# def get_team_schedule(standings, division_matchups, intra_conf_matchups, inter_conf_matchups, intra_conf_pairing, inter_conf_pairing):
#     """
#     Prompt for a team's short form and print the team's schedule in the order:
#     1. 6 games against division opponents
#     2. 4 games against intra-conference division opponents
#     3. 4 games against inter-conference division opponents
#     """
#     # Prompt for team short form
#     team_shortform = input("Enter the team's short form (e.g., JAX for Jacksonville Jaguars): ").upper()
    
#     # Find the team in standings
#     team = next((t for t in teams if t.shortform == team_shortform), None)
#     if not team:
#         print(f"Team with short form '{team_shortform}' not found.")
#         return

#     # Identify the team’s division and conference
#     team_conference = team.conference
#     team_division = team.division

#     print(f"\nSchedule for {team.full_name} ({team.shortform}, {team_conference} {team_division}):")

#     # 1. Division Matchups (6 games)
#     print(f"\nDivision Opponents (6 games against the {team_conference} {team_division}):")
#     for matchup in division_matchups:
#         if team in matchup:
#             opponent = matchup[1] if matchup[0] == team else matchup[0]
#             print(f"  - {opponent.full_name}")

#     # 2. Intra-Conference Matchups
#     intra_conf_division = intra_conf_pairing[team_conference][team_division]
#     print(f"\nIntra-Conference Opponents (4 games against the {team_conference} {intra_conf_division}):")
#     for matchup in intra_conf_matchups:
#         if team in matchup:
#             opponent = matchup[1] if matchup[0] == team else matchup[0]
#             print(f"  - {opponent.full_name}")

#     # 3. Inter-Conference Matchups
#     inter_conf_conference = "NFC" if team_conference == "AFC" else "AFC"
#     inter_conf_division = inter_conf_pairing[team_conference][team_division]
#     print(f"\nInter-Conference Opponents (4 games against the {inter_conf_conference} {inter_conf_division}):")
#     for matchup in inter_conf_matchups:
#         if team in matchup:
#             opponent = matchup[1] if matchup[0] == team else matchup[0]
#             print(f"  - {opponent.full_name}")

# standings = generate_random_standings()
# division_matchups = generate_division_matchups(standings)
# intra_conf_pairing, inter_conf_pairing = get_matchups(standings)
# intra_conf_matchups = generate_intra_conference_matchups(standings, intra_conf_pairing)
# inter_conf_matchups = generate_inter_conference_matchups(standings, inter_conf_pairing)

# get_team_schedule(standings, division_matchups, intra_conf_matchups, inter_conf_matchups, intra_conf_pairing, inter_conf_pairing)

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
    """Generate home-and-away matchups within each division (6 games per team)."""
    matchups = []
    for conference, divisions in standings.items():
        for division, teams in divisions.items():
            for i in range(len(teams)):
                for j in range(i + 1, len(teams)):
                    matchups.append((teams[i], teams[j]))
                    matchups.append((teams[j], teams[i]))
    return matchups

def generate_intra_conference_matchups(standings, intra_conf_pairing):
    """Generate matchups within the same conference for specific division pairings."""
    matchups = []
    for conference, division_pairings in intra_conf_pairing.items():
        for div1, div2 in division_pairings.items():
            division1_teams = standings[conference][div1]
            division2_teams = standings[conference][div2]
            for team1 in division1_teams:
                for team2 in division2_teams:
                    matchups.append((team1, team2))
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
    """Print the team’s schedule."""
    team_shortform = input("Enter the team's short form (e.g., JAX for Jacksonville Jaguars): ").upper()
    
    team = next((t for t in teams if t.shortform == team_shortform), None)
    if not team:
        print(f"Team with short form '{team_shortform}' not found.")
        return

    team_conference = team.conference
    team_division = team.division

    print(f"\nSchedule for {team.full_name} ({team.shortform}, {team_conference} {team_division}):")

    print(f"\nDivision Opponents (6 games against the {team_conference} {team_division}):")
    printed_opponents = set()
    for matchup in division_matchups:
        if team in matchup:
            opponent = matchup[1] if matchup[0] == team else matchup[0]
            if opponent not in printed_opponents:
                print(f"  - {opponent.full_name}")
                printed_opponents.add(opponent)

    intra_conf_division = intra_conf_pairing[team_conference][team_division]
    print(f"\nIntra-Conference Opponents (4 games against the {team_conference} {intra_conf_division}):")
    printed_opponents = set()
    for matchup in intra_conf_matchups:
        if team in matchup:
            opponent = matchup[1] if matchup[0] == team else matchup[0]
            if opponent not in printed_opponents:
                print(f"  - {opponent.full_name}")
                printed_opponents.add(opponent)

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
