import os
import zipfile
import re
import json

def brute_force():
    print("☢️ SRCL BRUTE FORCE MINER INITIATED")
    print("====================================")
    print("Scanning raw data streams in 'archives' and local ZIPs...")

    # Look in current folder and archives folder
    search_paths = [".", "archives"]
    
    # Regex patterns to find the "Gold" even if the file format is broken
    patterns = {
        'entropy': re.compile(rb'"entropy_A":\s*([-\d\.]+)'),
        'coherence': re.compile(rb'"coherence_A":\s*([-\d\.]+)'),
        'sharpe': re.compile(rb'Sharpe[:\s]+([-\d\.]+)'),
        'return': re.compile(rb'Return[:\s]+([-\d\.]+)')
    }

    hits = 0
    
    # We will store the best finds here
    best_physics = None
    best_trading = None
    max_coherence = -1.0
    max_sharpe = -10.0

    for path in search_paths:
        if not os.path.exists(path): continue
            
        for file in os.listdir(path):
            if file.endswith(".zip"):
                full_path = os.path.join(path, file)
                print(f"🔩 Drilling: {file}...")
                
                try:
                    with zipfile.ZipFile(full_path, 'r') as z:
                        for member in z.namelist():
                            try:
                                # READ RAW BYTES (Ignores file extension)
                                with z.open(member) as f:
                                    # Read first 10KB (enough to capture headers/stats)
                                    head = f.read(10000) 
                                    
                                    # 1. HUNT FOR PHYSICS (Entropy/Coherence)
                                    if b'entropy_A' in head:
                                        hits += 1
                                        ent = patterns['entropy'].search(head)
                                        coh = patterns['coherence'].search(head)
                                        
                                        if ent and coh:
                                            val_coh = float(coh.group(1))
                                            # print(f"   💎 PHYSICS DNA: Entropy {ent.group(1).decode()} | Coherence {val_coh} in {member}")
                                            
                                            # Track the "Most Structured" market
                                            if val_coh > max_coherence:
                                                max_coherence = val_coh
                                                best_physics = f"Entropy: {ent.group(1).decode()}, Coherence: {val_coh} (Source: {file}/{member})"
                                    
                                    # 2. HUNT FOR TRADING (Sharpe/Returns)
                                    if b'Sharpe' in head:
                                        hits += 1
                                        shp = patterns['sharpe'].search(head)
                                        ret = patterns['return'].search(head)
                                        
                                        if shp:
                                            val_shp = float(shp.group(1))
                                            val_ret = ret.group(1).decode() if ret else "?"
                                            print(f"   💰 TRADING DNA: Sharpe {val_shp} | Return {val_ret}% in {member}")
                                            
                                            # Track the "Most Profitable" Strategy
                                            if val_shp > max_sharpe:
                                                max_sharpe = val_shp
                                                best_trading = f"Sharpe: {val_shp}, Return: {val_ret}% (Source: {file}/{member})"

                            except:
                                continue
                except:
                    print(f"   ❌ Locked/Corrupt Zip: {file}")

    print("\n====================================")
    if hits > 0:
        print(f"✅ SUCCESS: {hits} Intelligence Artifacts Recovered.")
        print("\n🏆 BEST DISCOVERIES:")
        if best_physics:
            print(f"   1. BEST PHYSICS (Highest Structure): {best_physics}")
        if best_trading:
            print(f"   2. BEST STRATEGY (Highest Profit):   {best_trading}")
    else:
        print("⚠️ No data found. The archives might be empty or encrypted.")

if __name__ == "__main__":
    brute_force()
