#!/usr/bin/env python3
"""
plot_metrics.py
------------------------------------------------------
Plots SRCL environmental metrics from metrics_log.jsonl
------------------------------------------------------
"""

import json
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# === Locate latest log file ===
log_dir = Path("data/logs")
log_files = sorted(log_dir.glob("metrics_log.jsonl"))

if not log_files:
    raise FileNotFoundError("❌ No log files found in data/logs/ — run srcl_environmental_ripple.py first.")

log_path = log_files[-1]
print(f"📂 Using log file: {log_path}")

# === Load JSONL log file ===
data = []
with open(log_path, "r") as f:
    for line in f:
        try:
            data.append(json.loads(line.strip()))
        except json.JSONDecodeError:
            continue

df = pd.DataFrame(data)
print(f"✅ Loaded {len(df)} entries")

# === Compute rolling averages for smooth visualization ===
window = max(5, len(df) // 50)
df_smooth = df.rolling(window=window, min_periods=1).mean()

# === Plot ===
plt.figure(figsize=(10, 6))
plt.plot(df_smooth["step"], df_smooth["coherence_A"], label="Coherence (smoothness)", linewidth=1.8)
plt.plot(df_smooth["step"], df_smooth["entropy_A"], label="Entropy (complexity)", linewidth=1.8)
if "lyapunov_A" in df_smooth:
    plt.plot(df_smooth["step"], df_smooth["lyapunov_A"], label="Lyapunov (stability)", linewidth=1.8)
if "env_wave" in df_smooth:
    plt.plot(df_smooth["step"], df_smooth["env_wave"], label="Environment wave", linewidth=1.2, linestyle="--")

plt.title("🌊 SRCL Environmental Metrics Evolution")
plt.xlabel("Simulation Step")
plt.ylabel("Metric Value")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

# === Save plot ===
out_dir = Path("data/runs")
out_dir.mkdir(parents=True, exist_ok=True)
out_path = out_dir / "metrics_plot.png"
plt.savefig(out_path, dpi=200)
print(f"✅ Plot saved → {out_path}")
