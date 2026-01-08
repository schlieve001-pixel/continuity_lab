import os
import json
import re
import pandas as pd
import matplotlib.pyplot as plt
import glob

# KEYWORDS WE ARE HUNTING
PHYSICS_KEYS = ["entropy_A", "coherence_A", "alpha", "beta", "gamma"]
TRADING_KEYS = ["Sharpe", "Drawdown", "Return", "Win Rate"]

def deep_scan():
    print("🕵️ SRCL DEEP DRAGNET INITIATED")
    print("==============================")
    print("Scanning every file in repository for 'Lost Scrolls'...")
    
    root_dir = "."
    physics_data = []
    trading_data = []
    
    # 1. THE SEARCH
    # Walk through every folder and file
    for dirpath, _, filenames in os.walk(root_dir):
        # Skip git internals and virtual envs to speed up
        if ".git" in dirpath or "venv" in dirpath or "__pycache__" in dirpath:
            continue
            
        for file in filenames:
            filepath = os.path.join(dirpath, file)
            
            # Only check text-readable files
            if not file.endswith(('.json', '.txt', '.csv', '.log', '.md')):
                continue

            try:
                with open(filepath, 'r', errors='ignore') as f:
                    content = f.read()
                    
                    # A. HUNT FOR PHYSICS (The Revolution)
                    if '"entropy_A":' in content:
                        # Try to parse it as JSON lines
                        f.seek(0) # Reset to read line by line
                        for line in f:
                            if '"entropy_A":' in line:
                                try:
                                    json_obj = json.loads(line.strip())
                                    physics_data.append(json_obj)
                                except:
                                    pass
                        print(f"💎 PHYSICS DNA FOUND: {filepath}")

                    # B. HUNT FOR PROFITS (The Bank)
                    elif "Sharpe" in content and "Drawdown" in content:
                        # Extract the numbers using Regex
                        sharpe = re.search(r"Sharpe[:\s]+([\d\.-]+)", content)
                        ret = re.search(r"Return[:\s]+([\d\.-]+)%?", content)
                        if sharpe:
                            trading_data.append({
                                "file": filepath,
                                "sharpe": float(sharpe.group(1)),
                                "return": ret.group(1) if ret else "N/A"
                            })
                            print(f"💰 TRADING RECORD FOUND: {filepath}")
                            
            except Exception as e:
                continue

    # 2. THE COMPILATION
    print("\n📊 INTELLIGENCE REPORT")
    print("======================")
    print(f"🔹 Physics Datapoints Extracted: {len(physics_data)}")
    print(f"🔹 Trading Backtests Recovered: {len(trading_data)}")
    
    # 3. VISUALIZE THE SINGULARITY (If Physics found)
    if len(physics_data) > 10:
        print("\n🧪 PLOTTING THE SINGULARITY...")
        df = pd.DataFrame(physics_data)
        
        # Sort by step if available
        if 'step' in df.columns:
            df = df.sort_values('step')
            
        plt.figure(figsize=(12, 6))
        
        # Plot Entropy (Disorder)
        plt.subplot(2, 1, 1)
        plt.plot(df['step'], df['entropy_A'], color='red', label='Entropy (Market Turbulence)')
        plt.title('SRCL MARKET PHYSICS: The "Dead Zone" Crash Event')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Plot Coherence (Structure)
        plt.subplot(2, 1, 2)
        plt.plot(df['step'], df['coherence_A'], color='blue', label='Coherence (Trend Structure)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig("singularity_proof.png")
        print("✅ Graph saved to 'singularity_proof.png'")
        
        # 4. EXTRACT CONSTANTS
        # Get the average Alpha/Beta/Gamma from the stable period
        last_row = df.iloc[-1]
        constants = {
            "alpha": last_row.get('alpha'),
            "beta": last_row.get('beta'),
            "gamma": last_row.get('gamma')
        }
        with open("physics_constants.json", "w") as f:
            json.dump(constants, f, indent=4)
        print("🧬 PHYSICS CONSTANTS SAVED to 'physics_constants.json'")
        print(f"   -> Alpha: {constants['alpha']}")
        print(f"   -> Beta:  {constants['beta']}")
        print(f"   -> Gamma: {constants['gamma']}")

    # 5. LIST TOP STRATEGIES
    if trading_data:
        print("\n🏆 TOP 3 RECOVERED STRATEGIES")
        # Sort by Sharpe
        trading_data.sort(key=lambda x: x['sharpe'], reverse=True)
        for i, strat in enumerate(trading_data[:3]):
            print(f"   {i+1}. Sharpe: {strat['sharpe']} | Return: {strat['return']} | File: {strat['file']}")

if __name__ == "__main__":
    deep_scan()
