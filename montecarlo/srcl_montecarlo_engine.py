#!/usr/bin/env python3
"""
SRCL Monte Carlo Engine v3
------------------------------------------------------------
Massively parallel parameter-space exploration for the SRCL
Environmental Ripple simulation.
Generates large-scale datasets of coherence, entropy, and pattern stability.
------------------------------------------------------------
"""

import os, json, random, subprocess, multiprocessing as mp
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from tqdm import tqdm

# ============================================================
# CONFIGURATION
# ============================================================

MONTE_CARLO_RUNS = 500  # 🔧 Start small (500) → Scale to 10_000 when stable
STEPS = 500             # Fewer steps for parallel efficiency
OUTPUT_DIR = Path("results_montecarlo_v3")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

RANGES = {
    "alpha": (0.05, 0.12),
    "beta":  (0.08, 0.12),
    "gamma": (0.3, 0.9),
    "D":     (0.6, 1.0),
}

# ============================================================
# SINGLE SIMULATION WORKER
# ============================================================

def run_single_sim(idx):
    """Run one SRCL simulation and return its averaged metrics."""
    params = {k: random.uniform(*v) for k, v in RANGES.items()}
    log_path = OUTPUT_DIR / f"log_{idx:05d}.jsonl"

    cmd = [
        "python", "srcl_core/srcl_environmental_ripple.py",
        "--alpha", str(params["alpha"]),
        "--beta", str(params["beta"]),
        "--gamma", str(params["gamma"]),
        "--D", str(params["D"]),
        "--log", str(log_path),
    ]

    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Parse the output
    try:
        with open(log_path, "r") as f:
            data = [json.loads(line) for line in f if line.strip()]
        if not data:
            return None
        avg_coh = np.mean([d["coherence_A"] for d in data if "coherence_A" in d])
        avg_ent = np.mean([d["entropy_A"] for d in data if "entropy_A" in d])
        result = {**params, "coherence": avg_coh, "entropy": avg_ent}
        return result
    except Exception as e:
        print(f"[{idx}] ⚠️ Error reading log: {e}")
        return None

# ============================================================
# PARALLEL EXECUTION
# ============================================================

def run_montecarlo():
    print(f"🎲 Running Monte Carlo with {MONTE_CARLO_RUNS} samples...")
    with mp.Pool(processes=max(2, mp.cpu_count() - 1)) as pool:
        results = list(tqdm(pool.imap(run_single_sim, range(MONTE_CARLO_RUNS)), total=MONTE_CARLO_RUNS))

    results = [r for r in results if r is not None]
    df = pd.DataFrame(results)
    csv_path = OUTPUT_DIR / "srcl_montecarlo_results.csv"
    df.to_csv(csv_path, index=False)
    print(f"\n✅ Monte Carlo complete. Saved → {csv_path}")

    # ========================================================
    # ANALYSIS VISUALIZATIONS
    # ========================================================
    plt.figure(figsize=(6, 5))
    plt.scatter(df["entropy"], df["coherence"], alpha=0.6)
    plt.title("Entropy vs Coherence")
    plt.xlabel("Entropy (avg)")
    plt.ylabel("Coherence (avg)")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "entropy_vs_coherence.png", dpi=200)

    plt.figure(figsize=(6, 5))
    plt.scatter(df["alpha"], df["gamma"], c=df["coherence"], cmap="plasma")
    plt.title("Coherence vs Alpha/Gamma")
    plt.xlabel("Alpha")
    plt.ylabel("Gamma")
    plt.colorbar(label="Coherence")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "coherence_vs_alpha_gamma.png", dpi=200)

    plt.figure(figsize=(6, 5))
    plt.hist(df["coherence"], bins=30, color="purple", alpha=0.7)
    plt.title("Coherence Distribution")
    plt.xlabel("Coherence")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "coherence_histogram.png", dpi=200)

    print("📊 Plots saved →", OUTPUT_DIR)

# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    run_montecarlo()
