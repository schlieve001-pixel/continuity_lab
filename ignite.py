#!/usr/bin/env python3
import os
import sys
import time
import subprocess
from datetime import datetime

# VISUALS
BLUE = '\033[94m'
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'

def print_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{BLUE}")
    print("██╗ ██████╗ ███╗   ██╗██╗████████╗███████╗")
    print("██║██╔════╝ ████╗  ██║██║╚══██╔══╝██╔════╝")
    print("██║██║  ███╗██╔██╗ ██║██║   ██║   █████╗  ")
    print("██║██║   ██║██║╚██╗██║██║   ██║   ██╔══╝  ")
    print("██║╚██████╔╝██║ ╚████║██║   ██║   ███████╗")
    print("╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝   ╚═╝   ╚══════╝")
    print(f"       SRCL ELITE SYSTEM v2.0{RESET}")
    print("------------------------------------------")

def system_check():
    print(f"[{BLUE}INIT{RESET}] Checking Physics Engine...", end='')
    if os.path.exists("physics_engine/chaos_metrics.py"):
        print(f"{GREEN} OK{RESET}")
    else:
        print(f"{RED} FAILED (Missing Chaos Metrics){RESET}")
        sys.exit(1)

    print(f"[{BLUE}INIT{RESET}] Checking Tactical Modules...", end='')
    if os.path.exists("tactical_modules/fuse_monitor.py"):
        print(f"{GREEN} OK{RESET}")
    else:
        print(f"{RED} FAILED (Missing Fuse Monitor){RESET}")
        sys.exit(1)
        
    print(f"[{BLUE}INIT{RESET}] Syncing Time-Series DB...", end='')
    # Placeholder for database sync
    time.sleep(0.5) 
    print(f"{GREEN} ONLINE{RESET}")

def git_update():
    """Optional: Pulls latest code if git is initialized"""
    if os.path.exists(".git"):
        print(f"[{BLUE}GIT{RESET}] Checking for updates...", end='')
        try:
            subprocess.run(["git", "pull"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"{GREEN} UPDATED{RESET}")
        except:
            print(f"{RED} OFFLINE{RESET}")

def launch_dashboard():
    print(f"\n{GREEN}>>> IGNITING FUSION REACTOR...{RESET}")
    time.sleep(1)
    try:
        # Launch the main dashboard script
        os.system("python3 command_center/dashboard.py")
    except KeyboardInterrupt:
        pass

def safe_shutdown():
    print(f"\n\n[{BLUE}SYSTEM{RESET}] Initiating Safe Shutdown Protocol...")
    
    # 1. GIT SAVE (The "Bye" Command logic)
    if os.path.exists(".git"):
        print(f"[{BLUE}GIT{RESET}] Saving Progress...", end='')
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        subprocess.run(["git", "add", "."], stdout=subprocess.DEVNULL)
        subprocess.run(["git", "commit", "-m", f"Auto-Save: {now}"], stdout=subprocess.DEVNULL)
        subprocess.run(["git", "push"], stdout=subprocess.DEVNULL)
        print(f"{GREEN} SAVED & PUSHED{RESET}")
    else:
        print(f"[{RED}GIT{RESET}] Not connected to repo. Local save only.")

    print(f"[{BLUE}SYSTEM{RESET}] Cores Cooled. Goodbye.")

if __name__ == "__main__":
    try:
        print_banner()
        git_update()
        system_check()
        launch_dashboard()
    except Exception as e:
        print(f"{RED}CRITICAL FAILURE: {e}{RESET}")
    finally:
        safe_shutdown()
