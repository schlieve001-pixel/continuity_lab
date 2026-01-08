#!/usr/bin/env python3
"""
SRCL-MQ Batch Test Runner
Author: Continuity Lab Research Pipeline
Purpose: Run multiple SRCL-MQ simulations with varying parameters (alpha, beta, gamma, D)
and store the resulting field images for phase-space analysis.
"""

import os
import subprocess
import json
import itertools
from datetime import datetime

# Base configuration
base_dir = os.path.expanduser("~/origin/continuity_lab")
results_root = os.path.join(base_dir, "batch_results")
os.makedirs(results_root, exist_ok=True)

# Parameters to sweep
alphas = [0.05, 0.08, 0.10]
gammas = [0.5, 0.7, 0.9]
betas  = [0.1]
Ds     = [0.8]

# Path to SRCL-MQ simulation script
srcl_script = os.path.join(base_dir, "srcl_mq.py")

# Log file
log_file = os.path.join(results_root, "batch_log.json")
batch_log = []

print("🧠 SRCL-MQ Batch Test Runner Started")
print(f"📂 Results directory: {results_root}\n")

# Generate parameter combinations
for alpha, beta, gamma, D in itertools.product(alphas, betas, gammas, Ds):
    tag = f"alpha{alpha}_beta{beta}_gamma{gamma}_D{D}"
    result_dir = os.path.join(results_root, f"results_{tag}")
    os.makedirs(result_dir, exist_ok=True)

    print(f"🚀 Running simulation: {tag}")
    env = os.environ.copy()
    env["SRCL_ALPHA"] = str(alpha)
    env["SRCL_BETA"] = str(beta)
    env["SRCL_GAMMA"] = str(gamma)
    env["SRCL_D"] = str(D)
    env["SRCL_OUTDIR"] = result_dir

    # Run the SRCL-MQ simulation
    result = subprocess.run(
        ["python3", srcl_script],
        cwd=base_dir,
        env=env,
        capture_output=True,
        text=True,
    )

    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "tag": tag,
        "alpha": alpha,
        "beta": beta,
        "gamma": gamma,
        "D": D,
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }
    batch_log.append(log_entry)

    print(f"✅ Completed: {tag}\n")

# Save batch metadata
with open(log_file, "w") as f:
    json.dump(batch_log, f, indent=2)

print("📦 All simulations completed.")
print(f"📝 Log saved to: {log_file}")

# Zip all results
archive_path = os.path.join(base_dir, "srclmq_batch_results.zip")
print(f"🗜️  Archiving results into {archive_path}...")
subprocess.run(["zip", "-r", archive_path, results_root])

print("✅ Batch run and archive complete.")
