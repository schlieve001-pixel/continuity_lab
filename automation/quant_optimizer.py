"""
SRCL ELITE - HUNTER MODE v2 (Positive Skew Edition)
---------------------------------------------------
1. Constraint: Take Profit must be > 1.5x Stop Loss.
2. Forces the AI to hunt for BIG trends, not small scalps.
3. Target: Sharpe > 1.0 | Profit > 100%
"""

import random
import json
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from srcl_core.backtest_engine import QuantEngine

POPULATION_SIZE = 50
GENERATIONS = 30
TICKER = "BTC-USD"

print(f"🚀 Initializing HUNTER v2 (Positive Skew) for {TICKER}...")
engine = QuantEngine(ticker=TICKER)

def generate_skewed_genome():
    """Generates strategies that aim for HOME RUNS (Reward > Risk)."""
    
    # 1. Pick a Risk Level (Stop Loss)
    sl_mult = random.uniform(1.0, 3.0) 
    
    # 2. Force Reward to be 1.5x to 4x the Risk
    tp_mult = sl_mult * random.uniform(1.5, 4.0)
    
    return {
        'w_trend': random.uniform(0.4, 1.0),
        'w_mean_rev': random.uniform(0.4, 1.0),
        'w_vol': random.uniform(0.4, 1.0),
        'rsi_period': random.randint(5, 20),
        'buy_thresh': random.uniform(0.05, 0.25),
        'sell_thresh': random.uniform(0.05, 0.25),
        'sl_multiplier': sl_mult,
        'tp_multiplier': tp_mult
    }

def mutate(genome):
    new_genome = genome.copy()
    if random.random() < 0.2:
        k = random.choice(list(genome.keys()))
        
        # Mutate the value
        if 'period' in k:
            new_genome[k] = max(4, min(25, int(genome[k] + random.choice([-2, 2]))))
        elif 'multiplier' in k:
             new_genome[k] = max(1.0, genome[k] + random.uniform(-0.5, 0.5))
        else:
            new_genome[k] = max(0.1, min(1.0, genome[k] + random.uniform(-0.1, 0.1)))
            
    # --- CRITICAL: RE-ENFORCE POSITIVE SKEW ---
    # If mutation broke the rule (Reward < 1.5x Risk), fix it.
    if new_genome['tp_multiplier'] < (new_genome['sl_multiplier'] * 1.5):
        new_genome['tp_multiplier'] = new_genome['sl_multiplier'] * random.uniform(1.5, 3.0)
        
    return new_genome

def run_pipeline():
    population = [generate_skewed_genome() for _ in range(POPULATION_SIZE)]
    best_overall = -9999.0
    best_genome = None

    print(f"\n🧬 HUNTING STARTED: Force Reward > 1.5x Risk")
    print("-" * 60)

    for gen in range(1, GENERATIONS + 1):
        scored_pop = []
        for genome in population:
            score = engine.run_backtest(genome)
            scored_pop.append((genome, score))
        
        scored_pop.sort(key=lambda x: x[1], reverse=True)
        
        if scored_pop[0][1] > best_overall:
            best_overall = scored_pop[0][1]
            best_genome = scored_pop[0][0]
            
        valid_scores = [s[1] for s in scored_pop if s[1] > -900]
        avg_score = sum(valid_scores)/len(valid_scores) if valid_scores else -999
        
        print(f"Gen {gen:02d}: Best Score: {scored_pop[0][1]:.4f} | Avg: {avg_score:.4f}")
        
        survivors = [s[0] for s in scored_pop[:15]] 
        next_gen = survivors[:]
        while len(next_gen) < POPULATION_SIZE:
            next_gen.append(mutate(survivors[random.randint(0, len(survivors)-1)]))
        population = next_gen

    print("-" * 60)
    print("💾 SAVING WINNER...")
    engine.save_params(best_genome)
    
    print("\n🕵️ FINAL AUDIT...")
    stats = engine.run_backtest(best_genome, detailed_report=True)
    
    print("\n📊 SRCL POSITIVE SKEW AUDIT")
    print("=" * 40)
    print(f"💰 Final Balance:    ${stats['Final Balance']:,.2f}")
    print(f"📈 Total Return:     {stats['Total Return %']:.2f}%")
    print(f"📉 Max Drawdown:     {stats['Max Drawdown %']:.2f}%")
    print(f"🔄 Total Trades:     {stats['Trades']}")
    print(f"🔢 Sharpe Ratio:     {stats['Sharpe']:.4f}")
    print(f"⚖️ Risk Ratio:       1 : {best_genome['tp_multiplier']/best_genome['sl_multiplier']:.2f}")
    print("=" * 40)

if __name__ == "__main__":
    run_pipeline()
