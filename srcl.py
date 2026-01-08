import numpy as np
import matplotlib
matplotlib.use("Agg")  # headless mode (no display)
import matplotlib.pyplot as plt
from scipy.ndimage import laplace
from pathlib import Path

def run_srcl_memory(
    grid=120, steps=500,
    D=0.2, alpha=0.3, beta=1.0, gamma=0.4, k=0.7,
    dt=0.02, noise=0.05, memory_decay=0.97, memory_gain=0.05
):
    """
    SRCL-M: Self-Referential Continuity Lattice with Memory Feedback.
    Each cell remembers a weighted average of its past gradients (M),
    influencing its reflexivity (R). This allows emergent rhythmic structures.
    """

    results_dir = Path("~/origin/continuity_lab/results_srclm").expanduser()
    results_dir.mkdir(parents=True, exist_ok=True)

    # Fields
    C = np.random.uniform(-0.5, 0.5, (grid, grid))
    R = np.zeros_like(C)
    M = np.zeros_like(C)  # memory field

    print(f"🧠 Starting SRCL-M simulation: grid={grid}, steps={steps}")

    for t in range(steps):
        lapC = laplace(C, mode="wrap")
        lapR = laplace(R, mode="wrap")
        gradCx, gradCy = np.gradient(C)
        grad_mag = np.sqrt(gradCx**2 + gradCy**2)

        # Memory update: retain 97% of old memory + small portion of new gradient magnitude
        M = memory_decay * M + memory_gain * grad_mag

        # Reflexivity update
        dR = k * (np.tanh(M + np.abs(gradCx) + np.abs(gradCy)) - R)

        # Main field update (C coupled to R and memory)
        dC = D * lapC - alpha * C + beta * C**3 + gamma * R * lapR - 0.2 * M * C

        # Integrate
        C += dt * dC + noise * np.random.randn(*C.shape) * dt
        R += dt * dR

        if t % 100 == 0:
            print(f"🌀 Step {t}/{steps}")

            fig, ax = plt.subplots(1, 3, figsize=(10, 4))

            ax[0].imshow(C, cmap="coolwarm")
            ax[0].set_title(f"C (t={t})")
            ax[0].axis("off")

            ax[1].imshow(R, cmap="viridis")
            ax[1].set_title("Reflexivity R")
            ax[1].axis("off")

            ax[2].imshow(M, cmap="inferno")
            ax[2].set_title("Memory M")
            ax[2].axis("off")

            plt.tight_layout()
            output_path = results_dir / f"srclm_step_{t:04d}.png"
            plt.savefig(output_path)
            plt.close(fig)

    print("✅ SRCL-M complete! Check ~/origin/continuity_lab/results_srclm for output images.")

if __name__ == "__main__":
    run_srcl_memory()

