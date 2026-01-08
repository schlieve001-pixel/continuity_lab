#!/usr/bin/env python3
"""
SRCL Elite – Watchdog Agent
Continuously monitors core processes and restarts if needed.
"""

import subprocess, time, psutil, logging
from datetime import datetime

logging.basicConfig(filename="logs/watchdog.log", level=logging.INFO)

TARGETS = {
    "adaptive_montecarlo": "automation/adaptive_montecarlo.py",
    "optimizer": "automation/optimizer_agent.py"
}

def restart_process(name, cmd):
    logging.warning(f"[{datetime.now()}] Restarting {name}")
    subprocess.Popen(["python3", cmd])

def watchdog_loop():
    while True:
        for name, cmd in TARGETS.items():
            if not any(cmd in p.cmdline() for p in psutil.process_iter()):
                restart_process(name, cmd)
        time.sleep(60)

if __name__ == "__main__":
    watchdog_loop()
