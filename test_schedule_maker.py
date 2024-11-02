"""
PLEASE SEE: THIS FILE IS NO LONGER IN USE / NOT UPDATED
"""


# from schedule_maker import generate_random_standings, generate_division_matchups, generate_intra_conference_matchups, generate_inter_conference_matchups

# def test_generate_random_standings():
#     standings = generate_random_standings()
#     print("Randomized Standings by Division:")
#     for conference, divisions in standings.items():
#         print(f"Conference: {conference}")
#         for division, teams in divisions.items():
#             print(f"  Division: {division}")
#             for rank, team in enumerate(teams, 1):
#                 print(f"    {rank}: {team.full_name} ({team.shortform})")

# def test_generate_division_matchups():
#     standings = generate_random_standings()
#     division_matchups = generate_division_matchups(standings)
#     print("Division Matchups (Home and Away):")

#     # Group matchups by division for easier readability
#     for conference, divisions in standings.items():
#         print(f"\n=== {conference} Conference ===")
#         for division, teams in divisions.items():
#             print(f"\n--- {division} Division ---")
#             # Filter matchups for this specific division
#             for home, away in division_matchups:
#                 if home.division == division and home.conference == conference:
#                     print(f"{home.full_name} (Home) vs {away.full_name} (Away)")
#             print("\n")  # Extra break after each division for clarity

# def test_generate_intra_conference_matchups():
#     standings = generate_random_standings()
#     intra_conference_matchups = generate_intra_conference_matchups(standings)
#     print("\nIntra-Conference Matchups (2 Home and 2 Away):")

#     for conference, divisions in standings.items():
#         print(f"\n=== {conference} Conference ===")

#         # We are using a set of seen pairs to avoid redundant display and check variation
#         seen_pairs = set()

#         # Display each matchup for division pairs
#         division_keys = list(divisions.keys())
#         for i in range(0, len(division_keys), 2):
#             div1, div2 = division_keys[i], division_keys[i + 1]
#             pair = (div1, div2)
#             if pair not in seen_pairs:
#                 print(f"\n--- Matchup: {div1} Division vs {div2} Division ---")
#                 seen_pairs.add(pair)
                
#                 # Print only relevant matchups for this division pairing
#                 for home, away in intra_conference_matchups:
#                     if (home.division == div1 and away.division == div2) or \
#                        (home.division == div2 and away.division == div1):
#                         print(f"{home.full_name} (Home) vs {away.full_name} (Away)")
#                 print("\n")  # Extra break for clarity

# def test_generate_inter_conference_matchups():
#     standings = generate_random_standings()
#     inter_conference_matchups = generate_inter_conference_matchups(standings)
#     print("\nInter-Conference Matchups (AFC vs NFC):")

#     # Display matchups with AFC and NFC pairings
#     for afc_team, nfc_team in inter_conference_matchups:
#         print(f"{afc_team.full_name} ({afc_team.conference}) vs {nfc_team.full_name} ({nfc_team.conference})")

# if __name__ == "__main__":
#     #test_generate_random_standings()
#     #test_generate_division_matchups()
#     #test_generate_intra_conference_matchups()
#     test_generate_inter_conference_matchups()