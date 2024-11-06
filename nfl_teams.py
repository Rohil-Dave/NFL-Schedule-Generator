"""
NFL Teams Data Module

This module contains the NFL_TEAMS data structure that organizes all NFL teams
by conference and division. The data structure is used throughout the schedule
generator to access team information and maintain league organization.

Data Structure:
    NFL_TEAMS (dict): A nested dictionary organizing NFL teams by conference and division
        Format:
        {
            conference (str): {
                division (str): [
                    {
                        "name": str,          # Full team name
                        "abbreviation": str,  # Team abbreviation code
                        "conference": str,    # 'AFC' or 'NFC'
                        "division": str       # 'North', 'South', 'East', or 'West'
                    },
                    ...
                ]
            }
        }

Example:
    >>> NFL_TEAMS['AFC']['North'][0]
    {
        'name': 'Baltimore Ravens',
        'abbreviation': 'BAL',
        'conference': 'AFC',
        'division': 'North'
    }
"""
NFL_TEAMS = {
    "AFC": {
        "North": [
            {"name": "Baltimore Ravens", "abbreviation": "BAL", "conference": "AFC", "division": "North"},
            {"name": "Cincinnati Bengals", "abbreviation": "CIN", "conference": "AFC", "division": "North"},
            {"name": "Cleveland Browns", "abbreviation": "CLE", "conference": "AFC", "division": "North"},
            {"name": "Pittsburgh Steelers", "abbreviation": "PIT", "conference": "AFC", "division": "North"}
        ],
        "South": [
            {"name": "Houston Texans", "abbreviation": "HOU", "conference": "AFC", "division": "South"},
            {"name": "Indianapolis Colts", "abbreviation": "IND", "conference": "AFC", "division": "South"},
            {"name": "Jacksonville Jaguars", "abbreviation": "JAX", "conference": "AFC", "division": "South"},
            {"name": "Tennessee Titans", "abbreviation": "TEN", "conference": "AFC", "division": "South"}
        ],
        "East": [
            {"name": "Buffalo Bills", "abbreviation": "BUF", "conference": "AFC", "division": "East"},
            {"name": "Miami Dolphins", "abbreviation": "MIA", "conference": "AFC", "division": "East"},
            {"name": "New England Patriots", "abbreviation": "NE", "conference": "AFC", "division": "East"},
            {"name": "New York Jets", "abbreviation": "NYJ", "conference": "AFC", "division": "East"}
        ],
        "West": [
            {"name": "Denver Broncos", "abbreviation": "DEN", "conference": "AFC", "division": "West"},
            {"name": "Kansas City Chiefs", "abbreviation": "KC", "conference": "AFC", "division": "West"},
            {"name": "Las Vegas Raiders", "abbreviation": "LV", "conference": "AFC", "division": "West"},
            {"name": "Los Angeles Chargers", "abbreviation": "LAC", "conference": "AFC", "division": "West"}
        ]
    },
    "NFC": {
        "North": [
            {"name": "Chicago Bears", "abbreviation": "CHI", "conference": "NFC", "division": "North"},
            {"name": "Detroit Lions", "abbreviation": "DET", "conference": "NFC", "division": "North"},
            {"name": "Green Bay Packers", "abbreviation": "GB", "conference": "NFC", "division": "North"},
            {"name": "Minnesota Vikings", "abbreviation": "MIN", "conference": "NFC", "division": "North"}
        ],
        "South": [
            {"name": "Atlanta Falcons", "abbreviation": "ATL", "conference": "NFC", "division": "South"},
            {"name": "Carolina Panthers", "abbreviation": "CAR", "conference": "NFC", "division": "South"},
            {"name": "New Orleans Saints", "abbreviation": "NO", "conference": "NFC", "division": "South"},
            {"name": "Tampa Bay Buccaneers", "abbreviation": "TB", "conference": "NFC", "division": "South"}
        ],
        "East": [
            {"name": "Dallas Cowboys", "abbreviation": "DAL", "conference": "NFC", "division": "East"},
            {"name": "New York Giants", "abbreviation": "NYG", "conference": "NFC", "division": "East"},
            {"name": "Philadelphia Eagles", "abbreviation": "PHI", "conference": "NFC", "division": "East"},
            {"name": "Washington Commanders", "abbreviation": "WAS", "conference": "NFC", "division": "East"}
        ],
        "West": [
            {"name": "Arizona Cardinals", "abbreviation": "ARI", "conference": "NFC", "division": "West"},
            {"name": "Los Angeles Rams", "abbreviation": "LAR", "conference": "NFC", "division": "West"},
            {"name": "San Francisco 49ers", "abbreviation": "SF", "conference": "NFC", "division": "West"},
            {"name": "Seattle Seahawks", "abbreviation": "SEA", "conference": "NFC", "division": "West"}
        ]
    }
}