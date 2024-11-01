from data import teams, conferences

def test_team_data():
    print("Total number of teams:", len(teams))
    print("Sample team details:")
    for team in teams[:5]:  # Print the first 5 teams for quick verification
        print(f"{team.full_name} - {team.shortform} - {team.conference} - {team.division}")

def test_conference_data():
    print("\nConference Structure Verification:")
    for conference, divisions in conferences.items():
        print(f"Conference: {conference}")
        for division, teams in divisions.items():
            print(f"  Division: {division} has {len(teams)} teams")
            for team in teams:
                print(f"    {team.full_name} ({team.shortform})")

# Run tests
if __name__ == "__main__":
    test_team_data()
    test_conference_data()
