#!/usr/bin/env python3
"""
system_check.py
Performs environment diagnostics for SRCL Elite.
"""
import os
from rich.console import Console
from rich.table import Table

console = Console()
REQUIRED_DIRS = [
    "automation", "datafusion", "data", "results", "results_montecarlo_v3", "archives"
]

def check_environment():
    table = Table(title="SRCL System Check")
    table.add_column("Path")
    table.add_column("Status")
    for d in REQUIRED_DIRS:
        if os.path.exists(d):
            table.add_row(d, "[green]OK[/]")
        else:
            table.add_row(d, "[red]Missing[/]")
    console.print(table)

if __name__ == "__main__":
    check_environment()
