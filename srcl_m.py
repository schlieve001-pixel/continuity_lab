import numpy as np
import matplotlib
matplotlib.use("Agg")  # headless mode (no GUI needed)
import matplotlib.pyplot as plt
from scipy.ndimage import laplace
from pathlib import Path

def run_srcl_quantum(
    grid=150, steps=600,
    D=0.15, alpha=0.25, beta=1.0, gamma=0.3, omega=2.0,
    dt=0.015, noise=0.03
):
    """
    SRCL-Q: Self-Referential Continuity Lattice (Quantum Drift Variant)
    Introduces a complex-valued field ψ(x, y) = A * exp(iθ)
    that evolves under coupled diffusion + phase interference.
    """

    results_dir = Path("~/origin/continuity_lab/results_srclq").expanduser()
    results_dir.mkdir(parents=True, exist_ok=True)

    # Initialize the complex wave field ψ = amplitude * exp(i * phase)
    A = np.random.rand(grid, grid)
    phase = np.random.rand(grid, grid) * 2 * np.pi
    psi = A * np.exp(1j * phase)

    # Reflexivity field
    R = np.zeros((grid, grid), dtype=float)

    print(f"⚛️ Starting SRCL-Q simulation: grid={grid}, steps={steps}")

    for t in range(steps):
        lap_psi = laplace(psi, mode="wrap")

        # Phase gradient magnitude (represents local “quantum flow”)
        gradx, grady = np.gradient(np.angle(psi))
        current_mag = np.sqrt(gradx**2 + grady**2)

        # Reflexivity field responds to wave intensity
        dR = gamma * (np.tanh(np.abs(psi)) - R)
        R += dt * dR

        # Main evolution equation
        dpsi = (
            1j * omega * psi
            + D * lap_psi
            - alpha * psi
            + beta * np.abs(psi)**2 * psi
            + 0.1j * R * psi
        )

        # Add complex stochastic noise
        noise_term = noise * (np.random.randn(*psi.shape) + 1j * np.random.randn(*psi.shape))
        psi += dt * dpsi + noise_term * dt

        # Normalize to avoid divergence
        psi /= (1e-8 + np.max(np.abs(psi)))

        if t % 100 == 0:
            print(f"🌊 Step {t}/{steps}")

            fig, ax = plt.subplots(1, 3, figsize=(11, 4))
            ax[0].imshow(np.abs(psi), cmap="inferno")
            ax[0].set_title(f"|ψ| Amplitude (t={t})")
            ax[0].axis("off")

            ax[1].imshow(np.angle(psi), cmap="twilight")
            ax[1].set_title("Phase θ")
            ax[1].axis("off")

            ax[2].imshow(R, cmap="plasma")
            ax[2].set_title("Reflexivity R")
            ax[2].axis("off")

            plt.tight_layout()
            plt.savefig(results_dir / f"srclq_step_{t:04d}.png")
            plt.close(fig)

    print("✅ SRCL-Q complete! Check ~/origin/continuity_lab/results_srclq for output images.")

if __name__ == "__main__":
    run_srcl_quantum()
