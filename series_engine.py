import numpy as np
from team_profiles import TeamProfileManager

class GameSimulator:
    def __init__(self, home_team_profile, away_team_profile, is_home_game):
        self.home_team = home_team_profile
        self.away_team = away_team_profile
        self.is_home_game = is_home_game

    def calculate_win_probability(self):
        # Base win probability using MOV and seeding difference
        base_home_prob = 0.5

        mov_diff = self.home_team.mov - self.away_team.mov
        seed_diff = self.away_team.seed - self.home_team.seed

        # Apply MOV impact (0.5% per point diff)
        base_home_prob += mov_diff * 0.005

        # Apply seed impact (2% per seed difference)
        base_home_prob += seed_diff * 0.02

        # Home court advantage
        if self.is_home_game:
            base_home_prob += 0.04  # 4% bump for home court

        # Clamp probability between 0.05 and 0.95
        base_home_prob = max(min(base_home_prob, 0.95), 0.05)

        return base_home_prob

    def simulate_game(self):
        home_win_chance = self.calculate_win_probability()
        result = np.random.rand() < home_win_chance
        went_to_ot = np.random.rand() < 0.12  # 12% chance of overtime
        return result, went_to_ot

class SeriesSimulator:
    def __init__(self, home_team_name, away_team_name, simulations=10000):
        self.manager = TeamProfileManager(csv_path='team_profiles_2025.csv')
        self.home_team_profile = self.manager.get_team(home_team_name)
        self.away_team_profile = self.manager.get_team(away_team_name)
        self.simulations = simulations
        self.series_results = {"4-0": 0, "4-1": 0, "4-2": 0, "4-3": 0}

    def simulate_series(self):
        for _ in range(self.simulations):
            home_wins = 0
            away_wins = 0
            fatigue_home = 0
            fatigue_away = 0

            home_schedule = [True, True, False, False, True, False, True]
            travel_games = [4, 5, 6]

            for game_number, is_home_game in enumerate(home_schedule):
                if home_wins == 4 or away_wins == 4:
                    break

                simulator = GameSimulator(
                    self.home_team_profile,
                    self.away_team_profile,
                    is_home_game
                )

                home_wins_game, went_to_ot = simulator.simulate_game()

                if home_wins_game:
                    home_wins += 1
                else:
                    away_wins += 1

            if home_wins > away_wins:
                total_games = home_wins + away_wins
                if total_games == 4:
                    self.series_results["4-0"] += 1
                elif total_games == 5:
                    self.series_results["4-1"] += 1
                elif total_games == 6:
                    self.series_results["4-2"] += 1
                else:
                    self.series_results["4-3"] += 1

    def get_results(self):
        total = sum(self.series_results.values())
        return {k: v / total for k, v in self.series_results.items()}

if __name__ == "__main__":
    # Example run
    series_simulator = SeriesSimulator(home_team_name='Celtics', away_team_name='Heat', simulations=10000)
    series_simulator.simulate_series()
    results = series_simulator.get_results()
    print("Series Win Probabilities:")
    for outcome, prob in results.items():
        print(f"Home team wins {outcome}: {prob*100:.2f}%")
