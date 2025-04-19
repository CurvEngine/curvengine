from monte_engine_core import MonteEngine
import csv
from datetime import datetime
import os
import matplotlib.pyplot as plt
import numpy as np

def sim_input():
    print("\nEnter your simulation card (e.g., Magic @ -245 with 67% win probability):")
    events = []
    while True:
        label = input("Label (e.g. Magic): ")
        prob = float(input("Win Probability (0.00 to 1.00): "))
        odds = int(input("Odds (e.g. -245 or +120): "))
        stake = int(input("Stake Amount (e.g. 100): "))
        events.append({
            "label": label,
            "probability": prob,
            "odds": odds,
            "stake": stake
        })
        more = input("Add another? (y/n): ").strip().lower()
        if more != 'y':
            break
    return events

def run_simulation(events):
    engine = MonteEngine(simulations=10000)
    results = engine.simulate_card(events)
    return results

def show_results(events, results):
    print("\n✨ Simulation Results:")
    print("----------------------------")
    for event in events:
        print(f"{event['label']}: {event['probability']*100:.1f}% chance, {event['odds']} odds, ${event['stake']} stake")
    print("----------------------------")
    print(f"Mean Profit: ${results['mean_profit']:.2f}")
    print(f"Chance of Profit: {results['prob_profit']*100:.2f}%")
    print(f"98% Confidence Interval: ${results['confidence_interval'][0]:.2f} to ${results['confidence_interval'][1]:.2f}")

def log_results(events, results, filename="simulation_log.csv"):
    timestamp = datetime.now().isoformat()
    path = os.path.join(os.path.dirname(__file__), filename)
    with open(path, mode='a', newline='') as file:
        writer = csv.writer(file)
        for event in events:
            writer.writerow([
                timestamp,
                event['label'],
                event['probability'],
                event['odds'],
                event['stake'],
                round(results['mean_profit'], 2),
                round(results['prob_profit'], 4),
                round(results['confidence_interval'][0], 2),
                round(results['confidence_interval'][1], 2)
            ])
    print(f"✅ Simulation logged to: {path}")

def plot_distribution(simulation_results):
    plt.figure(figsize=(10, 5))
    plt.hist(simulation_results['all_simulations'], bins=50, color='skyblue', edgecolor='black')
    plt.title("Profit Distribution Across 10,000 Simulations")
    plt.xlabel("Profit ($)")
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_cumulative_distribution(simulation_results):
    sorted_profits = np.sort(simulation_results['all_simulations'])
    cumulative = np.arange(1, len(sorted_profits)+1) / len(sorted_profits)
    plt.figure(figsize=(10, 5))
    plt.plot(sorted_profits, cumulative, color='green')
    plt.title("Cumulative Probability Distribution")
    plt.xlabel("Profit ($)")
    plt.ylabel("Probability of Earning ≤ x")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    events = sim_input()
    results = run_simulation(events)
    show_results(events, results)
    log_results(events, results)
    plot_distribution(results)
    plot_cumulative_distribution(results)
