#!/usr/bin/env python3
import os, subprocess, sys

def system_check():
    print("\n🔍 SRCL System Check")
    print("=" * 40)
    print("Working directory:", os.getcwd())
    print("Python executable:", sys.executable)
    os.system("git status -s")
    print("\n✅ Environment Verified.\n")

def main_menu():
    while True:
        print("""
🌍 === SRCL Command Center (Elite v2) ===
  1. Run Environmental Ripple Simulation
  2. Run Optimizer (Standard)
  3. Run Monte Carlo (Massive)
  4. Archive & Push Results
  5. Git Sync (Manual)
  6. Gemini Interpretation
  7. Gemini → Optimizer Bridge
  8. Run Optimizer (AI Feedback Mode)
  9. System Check
  0. Exit Command Center
""")
        choice = input("Select option: ").strip()

        if choice == "1":
            os.system("python srcl_core/srcl_environmental_ripple.py")
        elif choice == "2":
            os.system("python automation/optimizer_agent.py")
        elif choice == "3":
            os.system("python automation/adaptive_montecarlo.py")
        elif choice == "4":
            os.system("python automation/archive_with_meta.py && python automation/upload_to_gcs.py")
        elif choice == "5":
            os.system("git pull origin main && git push origin main")
        elif choice == "6":
            os.system("python gemini_interpreter.py")
        elif choice == "7":
            os.system("python automation/gemini_optimizer_bridge.py")
        elif choice == "8":
            os.system("python automation/gemini_optimizer_bridge.py && python automation/optimizer_agent.py")
        elif choice == "9":
            system_check()
        elif choice == "0":
            print("👋 Exiting Command Center. Stay coherent.")
            break
        else:
            print("❌ Invalid option, try again.")

if __name__ == "__main__":
    main_menu()
