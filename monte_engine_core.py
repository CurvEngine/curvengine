import numpy as np

class MonteEngine:
    def __init__(self, simulations=10000):
        self.simulations = simulations

    def simulate_event(self, probability, stake=100, odds=-110):
        outcomes = np.random.rand(self.simulations) < probability
        payouts = np.where(
            outcomes,
            self.calculate_payout(odds, stake),
            -stake
        )
        return payouts

    def calculate_payout(self, odds, stake):
        if odds < 0:
            return stake * (100 / abs(odds))
        else:
            return stake * (odds / 100)

    def simulate_card(self, events):
        all_profits = []
        for event in events:
            payouts = self.simulate_event(
                probability=event['probability'],
                stake=event.get('stake', 100),
                odds=event.get('odds', -110)
            )
            all_profits.append(payouts)
        total_profits = np.sum(all_profits, axis=0)
        return {
            'mean_profit': np.mean(total_profits),
            'prob_profit': np.mean(total_profits > 0),
            'confidence_interval': np.percentile(total_profits, [1, 99]),
            'all_simulations': total_profits
        }
