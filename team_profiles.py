import csv

class TeamProfile:
    def __init__(self, team, seed, wins, losses, mov, mol, home_wins, away_wins):
        self.team = team
        self.seed = int(seed)
        self.wins = int(wins)
        self.losses = int(losses)
        self.mov = float(mov)
        self.mol = float(mol)
        self.home_wins = int(home_wins)
        self.away_wins = int(away_wins)

class TeamProfileManager:
    def __init__(self, csv_path='team_profiles_2024.csv'):
        self.team_profiles = {}
        self.load_profiles(csv_path)

    def load_profiles(self, csv_path):
        with open(csv_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                profile = TeamProfile(
                    team=row['Team'],
                    seed=row['Seed'],
                    wins=row['Wins'],
                    losses=row['Losses'],
                    mov=row['MOV'],
                    mol=row['MOL'],
                    home_wins=row['Home Wins'],
                    away_wins=row['Away Wins']
                )
                self.team_profiles[profile.team] = profile

    def get_team(self, team_name):
        return self.team_profiles.get(team_name)

    def list_teams(self):
        return list(self.team_profiles.keys())

if __name__ == "__main__":
    manager = TeamProfileManager()
    teams = manager.list_teams()
    print("Available Teams:")
    for t in teams:
        print(t)

    profile = manager.get_team("Celtics")
    if profile:
        print(f"\nProfile for {profile.team}:")
        print(f"Seed: {profile.seed}, Wins: {profile.wins}, Losses: {profile.losses}, MOV: {profile.mov}, MOL: {profile.mol}, Home Wins: {profile.home_wins}, Away Wins: {profile.away_wins}")
