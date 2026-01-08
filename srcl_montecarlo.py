
import json
import os
import random
from datetime import datetime
from srcl_core.reaction_diffusion import simulate

LOG_PATH = "data/logs/reaction_output.jsonl"
NUM_RUNS = 25

def ensure_log_path():
    log_dir = os.path.dirname(LOG_PATH)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

def random_params():
    return {
        "feed": round(random.uniform(0.01, 0.09), 4),
        "kill": round(random.uniform(0.02, 0.07), 4),
        "du": round(random.uniform(0.1, 0.25), 4),
        "dv": round(random.uniform(0.05, 0.2), 4),
        "alpha": round(random.uniform(0.1, 1.5), 3),
        "beta": round(random.uniform(0.1, 1.5), 3),
        "steps": 2500,
        "size": 100
    }

def main():
    ensure_log_path()
    for i in range(NUM_RUNS):
        params = random_params()
        result = simulate(params)

        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "run_id": f"srcl_{i:03d}",
            "parameters": params,
            "metrics": {
                "entropy": result["entropy"],
                "coherence": result["coherence"]
            }
        }

        with open(LOG_PATH, "a") as f:
            f.write(json.dumps(log_entry) + "\n")

        print(f"[✓] Logged run {i+1}/{NUM_RUNS}")

if __name__ == "__main__":
    main()
