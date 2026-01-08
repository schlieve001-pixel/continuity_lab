import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.ndimage import laplace
from pathlib import Path

def run_srcl_mq(
    grid=150, steps=600,
    D=0.15, alpha=0.25, beta=1.0, gamma=0.3,
    omega=2.0, dt=0.015, noise=0.03
):
    """
    SRCL-MQ: Hybrid Memory-Quantum Continuity Field.
    Combines real-valued memory M with complex wave ψ.
    """

    results_dir = Path("~/origin/continuity_lab/results_srclmq").expanduser()
    results_dir.mkdir(parents=True, exist_ok=True)

    A = np.random.rand(grid, grid)
    phase = np.random.rand(grid, grid) * 2 * np.pi
    psi = A * np.exp(1j * phase)
    M = np.zeros((grid, grid))
    R = np.zeros((grid, grid))

    print(f"🧩 Starting SRCL-MQ simulation: grid={grid}, steps={steps}")

    for t in range(steps):
        lap_psi = laplace(psi, mode="wrap")
        gradx, grady = np.gradient(np.angle(psi))
        coherence = np.exp(-0.5*(gradx**2 + grady**2))

        dR = gamma * (np.tanh(np.abs(psi)) - R)
        R += dt * dR
        M = 0.97*M + 0.03*np.abs(psi)

        dpsi = (
            1j*omega*psi
            + D*lap_psi
            - alpha*psi
            + beta*np.abs(psi)**2*psi
            + 0.1j*R*psi
            + 0.05*M*psi
        )

        noise_term = noise*(np.random.randn(*psi.shape)+1j*np.random.randn(*psi.shape))
        psi += dt*dpsi + noise_term*dt
        psi /= (1e-8 + np.max(np.abs(psi)))

        if t % 100 == 0:
            print(f"🔁 Step {t}/{steps}")
            fig, ax = plt.subplots(1, 3, figsize=(11, 4))
            ax[0].imshow(np.abs(psi), cmap="inferno")
            ax[0].set_title(f"|ψ| amplitude (t={t})"); ax[0].axis("off")
            ax[1].imshow(np.angle(psi), cmap="twilight")
            ax[1].set_title("phase θ"); ax[1].axis("off")
            ax[2].imshow(M, cmap="viridis")
            ax[2].set_title("memory field M"); ax[2].axis("off")
            plt.tight_layout()
            plt.savefig(results_dir / f"srclmq_step_{t:04d}.png")
            plt.close(fig)

    print("✅ SRCL-MQ complete!  Check ~/origin/continuity_lab/results_srclmq for images.")

if __name__ == "__main__":
    run_srcl_mq()

