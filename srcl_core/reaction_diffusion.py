
"""
reaction_diffusion.py
Core Gray-Scott Reaction-Diffusion PDE Solver for SRCL Elite Environment
"""

import numpy as np
from numba import njit, prange
from tqdm import tqdm

@njit(parallel=True)
def laplacian(Z):
    """Compute discrete Laplacian using direct neighbor access (Numba-safe)."""
    n, m = Z.shape
    L = np.zeros_like(Z)
    for i in prange(1, n - 1):
        for j in range(1, m - 1):
            L[i, j] = (
                Z[i - 1, j] + Z[i + 1, j] +
                Z[i, j - 1] + Z[i, j + 1] -
                4.0 * Z[i, j]
            )
    return L

@njit
def evolve(U, V, Du, Dv, F, k, dt, steps):
    for _ in range(steps):
        Lu = laplacian(U)
        Lv = laplacian(V)

        # Gray-Scott equations
        uvv = U * V * V
        U += (Du * Lu - uvv + F * (1 - U)) * dt
        V += (Dv * Lv + uvv - (F + k) * V) * dt

        # Boundary conditions (wraparound stabilization)
        U[0, :] = U[-2, :]
        U[-1, :] = U[1, :]
        U[:, 0] = U[:, -2]
        U[:, -1] = U[:, 1]

        V[0, :] = V[-2, :]
        V[-1, :] = V[1, :]
        V[:, 0] = V[:, -2]
        V[:, -1] = V[:, 1]

    return U, V

def compute_entropy(U, V):
    """Entropy-like metric from the final concentration fields."""
    UV = U + V
    hist, _ = np.histogram(UV, bins=256, range=(0.0, 2.0), density=True)
    hist += 1e-8  # prevent log(0)
    return -np.sum(hist * np.log(hist))

def compute_coherence(U, V):
    """Dummy coherence measure for now (L2 norm difference)."""
    return np.sqrt(np.mean((U - V) ** 2))

def run_simulation(N=128, Du=0.16, Dv=0.08, F=0.035, k=0.065, dt=1.0, steps=10000, seed_size=10):
    U = np.ones((N, N), dtype=np.float32)
    V = np.zeros((N, N), dtype=np.float32)

    # Initial seeding
    center = N // 2
    r = seed_size // 2
    U[center - r:center + r, center - r:center + r] = 0.50
    V[center - r:center + r, center - r:center + r] = 0.25

    U, V = evolve(U, V, Du, Dv, F, k, dt, steps)

    return {
        "entropy": float(compute_entropy(U, V)),
        "coherence": float(compute_coherence(U, V))
    }

def simulate(params=None):
    """
    Wrapper for SRCL Monte Carlo compatibility.
    Accepts optional params dict for config overrides.
    """
    print("🔥 simulate() was called")
    if params is None:
        params = {}

    return run_simulation(
        N=params.get("size", 128),
        Du=params.get("du", 0.16),
        Dv=params.get("dv", 0.08),
        F=params.get("feed", 0.035),
        k=params.get("kill", 0.065),
        dt=1.0,
        steps=params.get("steps", 10000),
        seed_size=10
    )

