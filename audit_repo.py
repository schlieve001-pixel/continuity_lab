import os
import json
import pandas as pd
import glob
import re

def mine_repo():
    print("🕵️ SRCL DEEP RESEARCH MINER")
    print("===========================")
    
    # 1. Map the Territory
    root_dir = "."
    result_files = []
    
    # Look for all potential result artifacts
    patterns = [
        "**/*best_params*.json",
        "**/*results*.json",
        "**/*log*.txt",
        "**/analysis/*.csv"
    ]
    
    for pattern in patterns:
        result_files.extend(glob.glob(os.path.join(root_dir, pattern), recursive=True))
    
    print(f"📂 Found {len(result_files)} potential intelligence artifacts.")
    
    winning_genes = []
    
    # 2. Extract Intelligence
    for file_path in result_files:
        try:
            if file_path.endswith('.json'):
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    # Detect if this is a gene file
                    if isinstance(data, dict) and 'fitness' in str(data):
                        print(f"💎 FOUND DNA: {file_path}")
                        winning_genes.append(data)
                    elif 'sharpe' in str(data).lower():
                         print(f"📈 FOUND STATS: {file_path}")
                         winning_genes.append(data)
                         
            elif file_path.endswith('.csv') or file_path.endswith('.txt'):
                # Peek for keywords
                with open(file_path, 'r', errors='ignore') as f:
                    content = f.read(1000)
                    if "Sharpe" in content or "Drawdown" in content:
                        print(f"📜 FOUND LOG: {file_path}")
                        
        except Exception as e:
            pass

    print("\n🔬 DNA EXTRACTION SUMMARY")
    print("==========================")
    if not winning_genes:
        print("❌ No structured DNA found. We may need to re-run evolution.")
    else:
        print(f"✅ Extracted {len(winning_genes)} unique strategy genomes.")
        # Try to print the best one
        try:
            # Simple heuristic to find the best looking gene
            best_gene = str(winning_genes[0])[:500] 
            print(f"\n🧬 SAMPLE GENOME (First 500 chars):\n{best_gene}")
        except:
            pass

if __name__ == "__main__":
    mine_repo()
