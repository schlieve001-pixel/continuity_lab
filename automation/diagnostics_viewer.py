#!/usr/bin/env python3
"""
diagnostics_viewer.py
Interactive log viewer using Rich.
"""
import os
from rich.console import Console
from rich.prompt import Prompt
from rich.syntax import Syntax

console = Console()

def view_logs(log_dir="logs"):
    if not os.path.exists(log_dir):
        console.print(f"[red]No log directory found: {log_dir}[/]")
        return
    files = [f for f in os.listdir(log_dir) if f.endswith(".log") or f.endswith(".jsonl")]
    if not files:
        console.print("[yellow]No log files to display.[/]")
        return
    for i, f in enumerate(files):
        console.print(f"[cyan]{i+1}[/]. {f}")
    choice = Prompt.ask("Select log file", choices=[str(i+1) for i in range(len(files))])
    file = files[int(choice)-1]
    with open(os.path.join(log_dir, file)) as f:
        content = f.read()
    syntax = Syntax(content, "json" if file.endswith("jsonl") else "text", theme="monokai", line_numbers=True)
    console.print(syntax)

if __name__ == "__main__":
    view_logs()
