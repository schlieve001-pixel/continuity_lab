#!/usr/bin/env python3
"""
SRCL Elite – Colab Deployment Agent
Clones and configures the SRCL environment in Google Colab.
"""

import os, subprocess

REPO_URL = "https://github.com/schlieve001-pixel/continuity_lab.git"

def deploy_colab():
    subprocess.run(["git", "clone", REPO_URL], check=True)
    os.chdir("continuity_lab")
    subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)
    subprocess.run(["bash", "init_srcl_elite.sh"], check=True)
    print("✅ SRCL deployed in Colab environment.")

if __name__ == "__main__":
    deploy_colab()
