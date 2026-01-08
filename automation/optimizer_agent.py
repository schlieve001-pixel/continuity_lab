# --- AT THE TOP OF THE FILE ---
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from srcl_core.backtest_engine import QuantEngine

# Initialize Engine (Load data once to save speed)
engine = QuantEngine("BTC-USD") # Or SPY, NVDA...

# --- INSIDE YOUR EVALUATION LOOP ---
def evaluate_genome(genome):
    """
    Decodes the DNA into trading parameters and asks the QuantEngine for the score.
    """
    # 1. Decode Genome (Example mapping, adjust to your GA structure)
    params = {
        'w_trend': genome[0],      # Gene 0: Weight of Trend
        'w_mean_rev': genome[1],   # Gene 1: Weight of RSI
        'w_vol': genome[2],        # Gene 2: Weight of Volatility
        'rsi_period': int(genome[3] * 30) + 5, # Map 0-1 to 5-35 period
        'buy_thresh': genome[4],
        'sell_thresh': genome[5]
    }
    
    # 2. Run Backtest
    sharpe_ratio = engine.run_backtest(params)
    
    # 3. Return Fitness (The GA maximizes this)
    return sharpe_ratio
#!/usr/bin/env python3
"""
optimizer_agent.py
Simple genetic optimizer for SRCL Elite.
"""
import random, json, os
from rich.console import Console

console = Console()

def fitness(params):
    # Placeholder fitness function
    # Replace this with real call to srcl.run_simulation()
    alpha, beta, gamma, D = params
    return -((alpha - 0.5)**2 + (beta - 1)**2 + (gamma - 0.8)**2 + (D - 0.01)**2)

def mutate(params):
    return [p + random.uniform(-0.05, 0.05) for p in params]

def crossover(p1, p2):
    return [(a + b) / 2 for a, b in zip(p1, p2)]

def run_optimizer(generations=20, pop_size=10):
    population = [[random.random() for _ in range(4)] for _ in range(pop_size)]
    for gen in range(generations):
        population = sorted(population, key=fitness, reverse=True)
        best = population[0]
        console.print(f"[cyan]Gen {gen+1}[/]: Best fitness {fitness(best):.4f}")
        new_pop = population[:2]
        while len(new_pop) < pop_size:
            p1, p2 = random.sample(population[:5], 2)
            child = mutate(crossover(p1, p2))
            new_pop.append(child)
        population = new_pop
    with open("analysis/best_params.json", "w") as f:
        json.dump(best, f)
    console.print(f"[green]✅ Optimization complete.[/] Best: {best}")

if __name__ == "__main__":
    os.makedirs("analysis", exist_ok=True)
    run_optimizer()
