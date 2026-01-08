#!/usr/bin/env python3
"""
SRCL Elite – DataFusion Analytics
Aggregates and visualizes SRCL simulation outputs.
"""

import os, json, pandas as pd, matplotlib.pyplot as plt
from pathlib import Path

DATA_DIR = Path("results_montecarlo_v3")

def aggregate_results():
    rows = []
    for file in DATA_DIR.glob("log_*.jsonl"):
        with open(file) as f:
            for line in f:
                rows.append(json.loads(line))
    df = pd.DataFrame(rows)
    df.to_csv("data/aggregate_results.csv", index=False)
    print(f"✅ Aggregated {len(df)} rows.")
    plot_heatmap(df)

def plot_heatmap(df):
    plt.figure()
    plt.hist2d(df["alpha"], df["coherence"], bins=30)
    plt.title("SRCL Coherence vs Alpha Parameter")
    plt.xlabel("Alpha")
    plt.ylabel("Coherence")
    plt.savefig("data/coherence_heatmap.png")
    print("📊 Heatmap saved: data/coherence_heatmap.png")

if __name__ == "__main__":
    aggregate_results()
