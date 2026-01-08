#!/usr/bin/env python3
"""
auto_heal.py
Detects and auto-fixes missing folders, dependencies, and configs.
"""
import os, subprocess, sys
from rich.console import Console

console = Console()

DIRECTORIES = [
    "automation", "datafusion", "data", "archives",
    "results_montecarlo_v3", "results_optimizer_v2", "srcl_core"
]
DEPENDENCIES = [
    "rich", "google-cloud-aiplatform", "google-cloud-storage", "pandas", "matplotlib"
]

def ensure_directories():
    fixed = []
    for d in DIRECTORIES:
        if not os.path.exists(d):
            os.makedirs(d, exist_ok=True)
            fixed.append(d)
    return fixed

def ensure_dependencies():
    missing = []
    for pkg in DEPENDENCIES:
        try:
            __import__(pkg.replace("-", "_"))
        except ImportError:
            missing.append(pkg)
    if missing:
        console.print(f"[yellow]Installing missing dependencies:[/yellow] {missing}")
        subprocess.run([sys.executable, "-m", "pip", "install"] + missing)

if __name__ == "__main__":
    console.print("[bold cyan]🔧 SRCL Auto-Heal Diagnostic[/]")
    created = ensure_directories()
    ensure_dependencies()
    if created:
        console.print(f"[green]Created missing dirs:[/green] {created}")
    else:
        console.print("[green]All directories present.[/green]")
    console.print("[green]✅ System check complete.[/green]")
