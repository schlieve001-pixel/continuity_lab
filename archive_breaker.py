import os
import zipfile
import json
import re
import io

def break_archives():
    print("🔨 SRCL ARCHIVE BREAKER INITIATED")
    print("=================================")
    print("Drilling into ZIP vaults to recover lost Physics & Trading Data...")

    # We look for zips in the current folder and the 'archives' folder
    search_paths = [".", "archives"]
    
    physics_hits = []
    trading_hits = []
    
    for path in search_paths:
        if not os.path.exists(path):
            continue
            
        for file in os.listdir(path):
            if file.endswith(".zip"):
                full_path = os.path.join(path, file)
                print(f"🔩 Cracking open: {full_path}...")
                
                try:
                    with zipfile.ZipFile(full_path, 'r') as z:
                        # List all files inside the zip
                        for member in z.namelist():
                            # We only care about text/json/logs
                            if not member.endswith(('.json', '.txt', '.csv', '.log')):
                                continue
                            
                            try:
                                # Read the file directly from memory
                                with z.open(member) as f:
                                    # Decode bytes to string
                                    content = f.read().decode('utf-8', errors='ignore')
                                    
                                    # 1. HUNT PHYSICS DNA (entropy, coherence)
                                    if '"entropy_A":' in content:
                                        # Parse line by line to find the JSON
                                        lines = content.splitlines()
                                        for line in lines:
                                            if '"entropy_A":' in line:
                                                try:
                                                    data = json.loads(line.strip())
                                                    # Tag it with the source zip
                                                    data['source_archive'] = file
                                                    physics_hits.append(data)
                                                except:
                                                    pass
                                        # Only print once per file to avoid spam
                                        print(f"   💎 FOUND PHYSICS in internal file: {member}")

                                    # 2. HUNT TRADING DNA (Sharpe, Drawdown)
                                    elif "Sharpe" in content and "Return" in content:
                                        # Regex extraction
                                        sharpe_match = re.search(r"Sharpe[:\s]+([\d\.-]+)", content)
                                        return_match = re.search(r"Return[:\s]+([\d\.-]+)%?", content)
                                        
                                        if sharpe_match:
                                            trading_hits.append({
                                                "archive": file,
                                                "internal_file": member,
                                                "sharpe": float(sharpe_match.group(1)),
                                                "return": return_match.group(1) if return_match else "N/A"
                                            })
                                            print(f"   💰 FOUND TRADING LOG in internal file: {member}")

                            except Exception as e:
                                # Skip unreadable files
                                continue
                except Exception as e:
                    print(f"   ❌ Could not open zip: {e}")

    # --- REPORTING ---
    print("\n📦 VAULT EXTRACTION SUMMARY")
    print("==========================")
    print(f"🔹 Physics Datapoints Recovered: {len(physics_hits)}")
    print(f"🔹 Strategy Backtests Recovered: {len(trading_hits)}")

    # 1. SAVE PHYSICS CONSTANTS
    if len(physics_hits) > 0:
        # Find the last valid entry to get the "Stable" constants
        latest = physics_hits[-1]
        constants = {
            "alpha": latest.get("alpha"),
            "beta": latest.get("beta"),
            "gamma": latest.get("gamma"),
            "source": latest.get("source_archive")
        }
        
        with open("recovered_physics.json", "w") as f:
            json.dump(constants, f, indent=4)
        
        print(f"\n✅ RECOVERED REVOLUTIONARY CONSTANTS:")
        print(f"   Alpha: {constants['alpha']}")
        print(f"   Beta:  {constants['beta']}")
        print(f"   Gamma: {constants['gamma']}")
        print(f"   (Saved to recovered_physics.json)")

    # 2. SAVE TRADING DNA
    if len(trading_hits) > 0:
        trading_hits.sort(key=lambda x: x['sharpe'], reverse=True)
        top_strat = trading_hits[0]
        
        with open("recovered_strategy.json", "w") as f:
            json.dump(top_strat, f, indent=4)
            
        print(f"\n✅ RECOVERED INSTITUTIONAL STRATEGY:")
        print(f"   Best Sharpe: {top_strat['sharpe']}")
        print(f"   Return:      {top_strat['return']}")
        print(f"   Source:      {top_strat['archive']} -> {top_strat['internal_file']}")
        print(f"   (Saved to recovered_strategy.json)")

if __name__ == "__main__":
    break_archives()
