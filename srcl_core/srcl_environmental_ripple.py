#!/usr/bin/env python3
import numpy as np
from tqdm import trange
import json, os
import argparse

# ======================================================
#  SRCL Environmental Ripple + Lyapunov & Entropy Engine
# ======================================================

# --- Command-line argument parser ---
parser = argparse.ArgumentParser(description="SRCL Environmental Ripple Simulation")
parser.add_argument("--alpha", type=float, default=0.08, help="reaction rate alpha")
parser.add_argument("--beta", type=float, default=0.1, help="reaction rate beta")
parser.add_argument("--gamma", type=float, default=0.6, help="coupling rate gamma")
parser.add_argument("--D", type=float, default=0.9, help="diffusion coefficient")
parser.add_argument("--log", type=str, default="data/logs/metrics_log.jsonl", help="path to save metrics log")
args = parser.parse_args()

# --- Simulation constants ---
size = 200
steps = 1000
alpha, beta, gamma, D = args.alpha, args.beta, args.gamma, args.D
Da, Db, De = 1.0, 0.5, 0.25
feed, kill = 0.055, 0.062
env_coupling = 0.05

# --- Initialize fields ---
A = np.ones((size, size))
B = np.zeros((size, size))
E = np.zeros((size, size))

# initial condition blob
A[size//2-5:size//2+5, size//2-5:size//2+5] = 0.5
B[size//2-5:size//2+5, size//2-5:size//2+5] = 0.25

# --- Metrics ---
def coherence(field):
    gx, gy = np.gradient(field)
    return float(np.mean(np.sqrt(gx**2 + gy**2)))

def entropy(field):
    hist, _ = np.histogram(field, bins=100, range=(0, 1))
    p = hist / np.sum(hist)
    p = p[p > 0]
    return float(-np.sum(p * np.log2(p)))

# --- Environmental driver ---
def environment_wave(t):
    return np.sin(t / 50.0) * env_coupling

# --- Ensure log directory exists ---
os.makedirs(os.path.dirname(args.log), exist_ok=True)

# --- Simulation loop ---
for t in trange(steps, desc="🌊 Simulating Environmental Ripple"):
    # Laplacian diffusion for A, B
    laplace_A = (
        np.roll(A, 1, 0) + np.roll(A, -1, 0) +
        np.roll(A, 1, 1) + np.roll(A, -1, 1) - 4 * A
    )
    laplace_B = (
        np.roll(B, 1, 0) + np.roll(B, -1, 0) +
        np.roll(B, 1, 1) + np.roll(B, -1, 1) - 4 * B
    )

    # Reaction-diffusion updates
    dA = Da * laplace_A - A * B**2 + feed * (1 - A)
    dB = Db * laplace_B + A * B**2 - (kill + feed) * B

    # Update with time step
    A += dA * 0.1
    B += dB * 0.1

    # Environmental wave coupling
    E = environment_wave(t) * np.ones_like(E)
    A += gamma * E

    # Clamp for numerical stability
    A = np.clip(A, 0, 1)
    B = np.clip(B, 0, 1)

    # Compute metrics
    metrics = {
        "step": t,
        "coherence_A": coherence(A),
        "entropy_A": entropy(A),
        "alpha": alpha,
        "beta": beta,
        "gamma": gamma,
        "D": D
    }

    # Save metrics incrementally
    with open(args.log, "a") as f:
        json.dump(metrics, f)
        f.write("\n")

print(f"\n✅ Simulation complete. Log saved to: {args.log}")
