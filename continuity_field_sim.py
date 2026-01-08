import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import laplace

def run_continuity_sim(grid_size=100, steps=500, D=0.2, alpha=0.5, beta=1.0, dt=0.1, noise=0.05):
    """
    Simulates the PDE:
        dC/dt = D∇²C - αC + βC³ + noise
    """
    C = np.random.uniform(-1, 1, (grid_size, grid_size))  # initial field
    snapshots = []

    for t in range(steps):
        lap = laplace(C, mode='wrap')  # periodic boundary
        dCdt = D * lap - alpha * C + beta * (C**3)
        C += dt * dCdt + noise * np.random.randn(*C.shape) * dt

        if t % (steps // 5) == 0:
            snapshots.append(C.copy())
            print(f"Step {t}/{steps} done...")

    return snapshots

def plot_snapshots(snapshots, title="Continuity Field Evolution"):
    plt.figure(figsize=(15, 3))
    for i, snap in enumerate(snapshots):
        plt.subplot(1, len(snapshots), i+1)
        plt.imshow(snap, cmap='coolwarm', origin='lower')
        plt.title(f"t={i}")
        plt.axis('off')
    plt.suptitle(title)
    plt.show()

if __name__ == "__main__":
    snaps = run_continuity_sim(D=0.3, alpha=0.4, beta=1.2, steps=400)
    plot_snapshots(snaps)
