import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path
from PIL import Image
from scipy.stats import entropy

def analyze_srclmq_results(results_dir="~/origin/continuity_lab/results_srclmq"):
    """
    Analyzes SRCL-MQ simulation outputs for coherence and energy evolution.
    """
    results_dir = Path(results_dir).expanduser()
    output_dir = results_dir.parent / "analysis_srclmq"
    output_dir.mkdir(exist_ok=True)

    image_files = sorted(results_dir.glob("srclmq_step_*.png"))
    if not image_files:
        print("❌ No simulation images found. Run srcl_mq.py first.")
        return

    mean_energy = []
    phase_entropy = []
    memory_energy = []

    print(f"📊 Found {len(image_files)} frames to analyze...")

    for img_path in image_files:
        img = np.array(Image.open(img_path).convert("RGB")) / 255.0

        # Split into 3 panels
        h, w, _ = img.shape
        panel_w = w // 3
        psi_amp = np.mean(img[:, :panel_w])  # amplitude panel
        psi_phase = img[:, panel_w:2*panel_w, 0]  # red channel only for phase entropy proxy
        mem_field = np.mean(img[:, 2*panel_w:])   # memory field panel

        # Compute pseudo-entropy of phase
        hist, _ = np.histogram(psi_phase.flatten(), bins=50, range=(0, 1), density=True)
        p = hist + 1e-12
        H = entropy(p)

        mean_energy.append(psi_amp)
        phase_entropy.append(H)
        memory_energy.append(mem_field)

    steps = np.arange(len(image_files))

    print("📈 Generating analysis plots...")

    fig, ax = plt.subplots(3, 1, figsize=(8, 10))
    ax[0].plot(steps, mean_energy, label="Mean |ψ| Energy", linewidth=2)
    ax[0].set_ylabel("Energy")
    ax[0].grid(True)

    ax[1].plot(steps, phase_entropy, color="purple", label="Phase Entropy", linewidth=2)
    ax[1].set_ylabel("Entropy")
    ax[1].grid(True)

    ax[2].plot(steps, memory_energy, color="green", label="Memory Alignment", linewidth=2)
    ax[2].set_ylabel("Memory Strength")
    ax[2].set_xlabel("Timestep")
    ax[2].grid(True)

    for a in ax:
        a.legend()

    plt.tight_layout()
    plt.savefig(output_dir / "srclmq_analysis_plot.png")
    plt.close(fig)

    print(f"✅ Analysis complete! Saved to {output_dir}/srclmq_analysis_plot.png")

if __name__ == "__main__":
    analyze_srclmq_results()

