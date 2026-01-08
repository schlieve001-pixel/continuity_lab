import numpy as np
import json, os

def coherence(field):
    gx, gy = np.gradient(field)
    return float(np.mean(np.sqrt(gx**2 + gy**2)))

def entropy(field, bins=50):
    hist, _ = np.histogram(field, bins=bins, density=True)
    hist = hist[hist > 0]
    return float(-np.sum(hist * np.log(hist)))

def log_metrics(step, A, B, E, env_wave, outdir):
    metrics = {
        "step": step,
        "coherence_A": coherence(A),
        "coherence_B": coherence(B),
        "entropy_A": entropy(A),
        "entropy_B": entropy(B),
        "env_mean": float(np.mean(E)),
        "env_wave": env_wave
    }
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, "metrics_log.jsonl")
    with open(path, "a") as f:
        f.write(json.dumps(metrics) + "\n")
