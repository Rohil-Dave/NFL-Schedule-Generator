from schedule_maker import generate_random_standings

def test_generate_random_standings():
    standings = generate_random_standings()
    print("Randomized Standings by Division:")
    for conference, divisions in standings.items():
        print(f"Conference: {conference}")
        for division, teams in divisions.items():
            print(f"  Division: {division}")
            for rank, team in enumerate(teams, 1):
                print(f"    {rank}: {team.full_name} ({team.shortform})")

if __name__ == "__main__":
    test_generate_random_standings()