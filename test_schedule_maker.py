from schedule_maker import generate_random_standings, generate_division_matchups

def test_generate_random_standings():
    standings = generate_random_standings()
    print("Randomized Standings by Division:")
    for conference, divisions in standings.items():
        print(f"Conference: {conference}")
        for division, teams in divisions.items():
            print(f"  Division: {division}")
            for rank, team in enumerate(teams, 1):
                print(f"    {rank}: {team.full_name} ({team.shortform})")

def test_generate_division_matchups():
    standings = generate_random_standings()
    division_matchups = generate_division_matchups(standings)
    print("Division Matchups (Home and Away):")

    # Group matchups by division for easier readability
    for conference, divisions in standings.items():
        print(f"\n=== {conference} Conference ===")
        for division, teams in divisions.items():
            print(f"\n--- {division} Division ---")
            # Filter matchups for this specific division
            for home, away in division_matchups:
                if home.division == division and home.conference == conference:
                    print(f"{home.full_name} (Home) vs {away.full_name} (Away)")
            print("\n")  # Extra break after each division for clarity

if __name__ == "__main__":
    test_generate_random_standings()
    test_generate_division_matchups()