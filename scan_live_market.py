import pandas as pd
import glob
import os
import numpy as np
from srcl_core.god_mode import GodModeRegime

def scan_the_market():
    print("📡 SRCL GOD MODE: INITIATING LIVE SCAN")
    print("======================================")
    
    # 1. Initialize the Physics Engine
    engine = GodModeRegime()
    constants = engine.get_constants()
    print(f"🧬 LOADED CONSTANTS: Alpha={constants['alpha']:.3f} | Beta={constants['beta']:.3f}")
    
    # 2. Find Market Data
    data_path = "data/market_data/*.parquet"
    files = glob.glob(data_path)
    
    if not files:
        print("❌ No market data found. Run 'python srcl_core/market_data.py' first.")
        return

    print(f"🔍 Scanning {len(files)} assets for Singularity Structures...\n")

    # 3. The Scan Loop
    for f in files:
        asset = os.path.basename(f).replace("_processed.parquet", "")
        
        try:
            df = pd.read_parquet(f)
            
            # --- THE FIX: NORMALIZE COLUMNS ---
            # Convert 'Close', 'CLOSE', 'close' all to 'close'
            df.columns = [c.lower() for c in df.columns]
            
            if 'close' not in df.columns:
                print(f"⚠️ Skipped {asset}: 'close' price column missing.")
                continue
                
            # Ensure we have enough data
            if len(df) < 100: continue
            
            # Run the Physics Scan
            prices = df['close']
            signal = engine.scan_market(prices)
            
            # Physics Report
            log_ret = np.log(prices / prices.shift(1)).dropna()
            volatility = log_ret.std()
            
            # Visual Output
            if signal == "GOD_MODE_ENGAGE":
                status_icon = "🟢 **ENGAGE**"
            elif signal == "CRASH_PROTECTION":
                status_icon = "🔴 **CRASH RISK**"
            else:
                status_icon = "⚪ WAIT"
                
            print(f"📊 {asset}:")
            print(f"   -> Physics Status: {status_icon}")
            print(f"   -> Volatility:     {volatility:.5f} (Threshold: {constants['alpha']:.3f})")
            print(f"   -> Signal:         {signal}")
            print("--------------------------------------")
            
        except Exception as e:
            print(f"⚠️ Error reading {asset}: {e}")

    print("\n✅ SCAN COMPLETE.")

if __name__ == "__main__":
    scan_the_market()
