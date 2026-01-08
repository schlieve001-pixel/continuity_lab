#!/usr/bin/env python3
"""
SRCL Elite – Gemini → Optimizer Bridge
---------------------------------------
Closes the loop between Gemini (Vertex AI) insights and SRCL optimization engine.
Gemini reads simulation logs and outputs new parameter targets (α, β, γ, D)
that the optimizer_agent can use for its next generation.
"""

import json, os, glob
from pathlib import Path
from google.cloud import aiplatform
from vertexai.preview import generative_models as gm

# === CONFIG ===
PROJECT_ID = "canvas-sum-481614-f6"
LOCATION = "us-central1"
LOG_PATH = Path("results_montecarlo_v3")
OUTPUT_FILE = Path("data/next_parameters.json")
GEMINI_MODEL = "gemini-pro"

# Safety settings
MAX_CALLS_PER_HOUR = 5
FEEDBACK_MODE = True

def get_latest_logs(n=200):
    """Read the last N lines from the latest simulation log files."""
    files = sorted(glob.glob(str(LOG_PATH / "log_*.jsonl")), reverse=True)
    lines = []
    for f in files[:3]:  # look at last 3 logs
        with open(f) as fh:
            lines.extend(fh.readlines()[-n:])
    return [json.loads(l) for l in lines if l.strip()]

def ask_gemini_for_parameters(logs):
    """Send structured simulation data to Gemini and request new parameters."""
    aiplatform.init(project=PROJECT_ID, location=LOCATION)
    model = gm.GenerativeModel(GEMINI_MODEL)

    prompt = f"""
You are the SRCL Lab's scientific assistant.
Given recent simulation results, propose new optimized parameters
(alpha, beta, gamma, D) to maximize coherence and minimize entropy.
Return only valid JSON in this format:
{{
  "alpha": float,
  "beta": float,
  "gamma": float,
  "D": float,
  "reasoning": "brief explanation"
}}
Here are the latest data samples:
{json.dumps(logs[-10:], indent=2)}
"""

    response = model.generate_content(prompt)
    try:
        text = response.text.strip()
        parsed = json.loads(text[text.find("{"):text.rfind("}")+1])
        print("🧠 Gemini JSON recommendation:", parsed)
        return parsed
    except Exception as e:
        print(f"[⚠️ Gemini parse error] {e}")
        print("Raw output:", response.text)
        return None

def save_recommendation(rec):
    """Save Gemini’s new parameters to next_parameters.json."""
    OUTPUT_FILE.parent.mkdir(exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        json.dump(rec, f, indent=2)
    print(f"💾 Saved new parameters to {OUTPUT_FILE}")

def run_bridge():
    logs = get_latest_logs()
    if not logs:
        print("⚠️ No simulation logs found. Run Monte Carlo first.")
        return

    print(f"📡 Sending {len(logs)} samples to Gemini...")
    recommendation = ask_gemini_for_parameters(logs)
    if recommendation:
        save_recommendation(recommendation)
        if FEEDBACK_MODE:
            print("🔁 Ready for Optimizer to consume updated parameters.")
    else:
        print("❌ No valid recommendation produced.")

if __name__ == "__main__":
    run_bridge()
