"""
SRCL ELITE - HYDRA OPTIMIZER (Soft Constraints Edition)
-------------------------------------------------------
1. Loads BTC, ETH, SOL.
2. PENALIZES failures instead of killing them instantly.
3. Allows evolution to find a path through the chaos.
"""

import random
import json
import os
import sys
import pandas as pd
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from srcl_core.backtest_engine import QuantEngine

# CONFIGURATION
POPULATION_SIZE = 50
GENERATIONS = 30
ASSETS = ["BTC-USD", "ETH-USD", "SOL-USD"]

print(f"🐲 INITIALIZING SOFT HYDRA FOR: {ASSETS}")

engines = {}
for asset in ASSETS:
    try:
        engines[asset] = QuantEngine(ticker=asset)
        print(f"✅ Loaded {asset}")
    except Exception as e:
        print(f"❌ Could not load {asset}: {e}")

if len(engines) < 1:
    sys.exit("🚨 FATAL: No data found.")

def generate_hydra_genome():
    sl_mult = random.uniform(2.0, 5.0) # Wider stops for crypto
    tp_mult = sl_mult * random.uniform(1.2, 4.0) 
    
    return {
        'w_trend': random.uniform(0.1, 1.0),
        'w_mean_rev': random.uniform(0.1, 1.0),
        'w_vol': random.uniform(0.1, 1.0),
        'rsi_period': random.randint(5, 20),
        'buy_thresh': random.uniform(0.05, 0.3),
        'sell_thresh': random.uniform(0.05, 0.3),
        'sl_multiplier': sl_mult,
        'tp_multiplier': tp_mult
    }

def mutate(genome):
    new_genome = genome.copy()
    if random.random() < 0.3: # Higher mutation rate
        k = random.choice(list(genome.keys()))
        if 'period' in k:
            new_genome[k] = max(4, min(25, int(genome[k] + random.choice([-2, 2]))))
        elif 'multiplier' in k:
             new_genome[k] = max(1.5, genome[k] + random.uniform(-0.5, 0.5))
        else:
            new_genome[k] = max(0.05, min(1.0, genome[k] + random.uniform(-0.1, 0.1)))
            
    if new_genome['tp_multiplier'] < (new_genome['sl_multiplier'] * 1.1):
        new_genome['tp_multiplier'] = new_genome['sl_multiplier'] * 1.5
        
    return new_genome

def evaluate_hydra(genome):
    total_score = 0
    
    for asset, engine in engines.items():
        stats = engine.run_backtest(genome, detailed_report=True)
        
        # 1. HANDLE DEAD STRATEGIES
        if isinstance(stats, float): # If it returned -999.0
            total_score -= 20.0 # Heavy penalty, but not death
            continue
            
        sharpe = stats['Sharpe']
        profit = stats['Total Return %']
        drawdown = stats['Max Drawdown %']
        trades = stats['Trades']
        
        # 2. SCORING LOGIC
        asset_score = sharpe
        
        if profit < 0: 
            asset_score -= 5.0 # Penalty for losing money
        
        if drawdown < -35:
            asset_score -= 5.0 # Penalty for crashes
            
        if trades < 30:
            asset_score -= 2.0 # Penalty for laziness
            
        total_score += asset_score

    return total_score

def run_evolution():
    population = [generate_hydra_genome() for _ in range(POPULATION_SIZE)]
    best_overall = -9999.0
    best_genome = None

    print(f"\n🔥 SOFT HYDRA EVOLUTION STARTED")
    print("-" * 60)

    for gen in range(1, GENERATIONS + 1):
        scored_pop = []
        for genome in population:
            score = evaluate_hydra(genome)
            scored_pop.append((genome, score))
        
        scored_pop.sort(key=lambda x: x[1], reverse=True)
        
        if scored_pop[0][1] > best_overall:
            best_overall = scored_pop[0][1]
            best_genome = scored_pop[0][0]
            
        print(f"Gen {gen:02d}: Best Score: {scored_pop[0][1]:.4f}")
        
        survivors = [s[0] for s in scored_pop[:15]] 
        next_gen = survivors[:]
        while len(next_gen) < POPULATION_SIZE:
            next_gen.append(mutate(survivors[random.randint(0, len(survivors)-1)]))
        population = next_gen

    print("-" * 60)
    print("🏆 HYDRA WINNER FOUND")
    
    # Save to disk
    with open("automation/best_hydra_params.json", "w") as f:
        json.dump(best_genome, f, indent=2)

    # FINAL AUDIT (Crash Proof)
    print("\n📊 FINAL HYDRA AUDIT")
    for asset, engine in engines.items():
        stats = engine.run_backtest(best_genome, detailed_report=True)
        if isinstance(stats, float):
            print(f"🔹 {asset}: 💀 FAILED (Too few trades)")
        else:
            print(f"🔹 {asset}: Return {stats['Total Return %']:.1f}% | DD {stats['Max Drawdown %']:.1f}% | Trades {stats['Trades']} | Sharpe {stats['Sharpe']:.2f}")

if __name__ == "__main__":
    run_evolution()
