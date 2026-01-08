#!/usr/bin/env python3
"""
SRCL Elite – Archive With Metadata
Creates compressed archives with run configuration and dependency snapshots.
"""

import os, json, zipfile, subprocess
from datetime import datetime
from pathlib import Path

def archive_results():
    results_dir = Path("results_montecarlo_v3")
    archive_dir = Path("archives")
    archive_dir.mkdir(exist_ok=True)

    meta = {
        "timestamp": datetime.utcnow().isoformat(),
        "dependencies": subprocess.getoutput("pip freeze"),
        "seed": os.environ.get("SRCL_SEED", "N/A")
    }

    meta_path = results_dir / "meta.json"
    with open(meta_path, "w") as f:
        json.dump(meta, f, indent=2)

    zip_name = f"srcl_results_{datetime.utcnow().strftime('%Y%m%d_%H%M')}.zip"
    zip_path = archive_dir / zip_name

    with zipfile.ZipFile(zip_path, "w") as z:
        for file in results_dir.glob("**/*"):
            z.write(file, file.relative_to(results_dir))

    print(f"📦 Archived results to {zip_path}")
    return zip_path

if __name__ == "__main__":
    archive_results()

