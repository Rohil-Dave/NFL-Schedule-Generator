"""
This module defines the structure and data for NFL teams, organized by conference and division. 
Each team is represented as an instance of the `Team` class, storing information such as 
full name, location, shortform, conference, and division.

The `teams` list contains all 32 NFL teams, and the `conferences` dictionary organizes 
them by conference (AFC and NFC) and division (East, North, South, West) for easy access.

Classes:
    - Team: Represents an NFL team with attributes like full name, location, shortform, 
      conference, and division.

Data:
    - teams: A list of all NFL teams as `Team` instances.
    - conferences: A dictionary organizing teams by conference and division.
"""

class Team:
    def __init__(self, full_name, location, shortform, conference, division):
        self.full_name = full_name
        self.location = location
        self.shortform = shortform
        self.conference = conference
        self.division = division

# Creating all NFL teams with their respective information

# AFC Teams
# ----------------------------------------
# AFC East
teams = [
    Team("Buffalo Bills", "Buffalo, New York", "BUF", "AFC", "East"),
    Team("Miami Dolphins", "Miami, Florida", "MIA", "AFC", "East"),
    Team("New England Patriots", "Foxborough, Massachusetts", "NE", "AFC", "East"),
    Team("New York Jets", "East Rutherford, New Jersey", "NYJ", "AFC", "East"),

    # AFC North
    Team("Baltimore Ravens", "Baltimore, Maryland", "BAL", "AFC", "North"),
    Team("Cincinnati Bengals", "Cincinnati, Ohio", "CIN", "AFC", "North"),
    Team("Cleveland Browns", "Cleveland, Ohio", "CLE", "AFC", "North"),
    Team("Pittsburgh Steelers", "Pittsburgh, Pennsylvania", "PIT", "AFC", "North"),

    # AFC South
    Team("Houston Texans", "Houston, Texas", "HOU", "AFC", "South"),
    Team("Indianapolis Colts", "Indianapolis, Indiana", "IND", "AFC", "South"),
    Team("Jacksonville Jaguars", "Jacksonville, Florida", "JAX", "AFC", "South"),
    Team("Tennessee Titans", "Nashville, Tennessee", "TEN", "AFC", "South"),

    # AFC West
    Team("Denver Broncos", "Denver, Colorado", "DEN", "AFC", "West"),
    Team("Kansas City Chiefs", "Kansas City, Missouri", "KC", "AFC", "West"),
    Team("Las Vegas Raiders", "Las Vegas, Nevada", "LV", "AFC", "West"),
    Team("Los Angeles Chargers", "Inglewood, California", "LAC", "AFC", "West"),
    
    # NFC Teams
    # ----------------------------------------
    # NFC East
    Team("Dallas Cowboys", "Arlington, Texas", "DAL", "NFC", "East"),
    Team("New York Giants", "East Rutherford, New Jersey", "NYG", "NFC", "East"),
    Team("Philadelphia Eagles", "Philadelphia, Pennsylvania", "PHI", "NFC", "East"),
    Team("Washington Commanders", "Landover, Maryland", "WAS", "NFC", "East"),

    # NFC North
    Team("Chicago Bears", "Chicago, Illinois", "CHI", "NFC", "North"),
    Team("Detroit Lions", "Detroit, Michigan", "DET", "NFC", "North"),
    Team("Green Bay Packers", "Green Bay, Wisconsin", "GB", "NFC", "North"),
    Team("Minnesota Vikings", "Minneapolis, Minnesota", "MIN", "NFC", "North"),

    # NFC South
    Team("Atlanta Falcons", "Atlanta, Georgia", "ATL", "NFC", "South"),
    Team("Carolina Panthers", "Charlotte, North Carolina", "CAR", "NFC", "South"),
    Team("New Orleans Saints", "New Orleans, Louisiana", "NO", "NFC", "South"),
    Team("Tampa Bay Buccaneers", "Tampa, Florida", "TB", "NFC", "South"),

    # NFC West
    Team("Arizona Cardinals", "Glendale, Arizona", "ARI", "NFC", "West"),
    Team("Los Angeles Rams", "Inglewood, California", "LAR", "NFC", "West"),
    Team("San Francisco 49ers", "Santa Clara, California", "SF", "NFC", "West"),
    Team("Seattle Seahawks", "Seattle, Washington", "SEA", "NFC", "West")
]

# Organizing teams by conference and division for easy access
conferences = {
    "AFC": {
        "East": [team for team in teams if team.conference == "AFC" and team.division == "East"],
        "North": [team for team in teams if team.conference == "AFC" and team.division == "North"],
        "South": [team for team in teams if team.conference == "AFC" and team.division == "South"],
        "West": [team for team in teams if team.conference == "AFC" and team.division == "West"],
    },
    "NFC": {
        "East": [team for team in teams if team.conference == "NFC" and team.division == "East"],
        "North": [team for team in teams if team.conference == "NFC" and team.division == "North"],
        "South": [team for team in teams if team.conference == "NFC" and team.division == "South"],
        "West": [team for team in teams if team.conference == "NFC" and team.division == "West"],
    }
}
