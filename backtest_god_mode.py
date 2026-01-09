import pandas as pd
import glob
import os
import numpy as np
from srcl_core.god_mode import GodModeRegime

def run_physics_backtest():
    print("⏳ SRCL PHYSICS BACKTEST: REPLAYING HISTORY")
    print("=========================================")
    
    # 1. Setup Engine
    engine = GodModeRegime()
    constants = engine.get_constants()
    print(f"🧬 Testing DNA: Alpha={constants['alpha']:.3f} | Beta={constants['beta']:.3f}")
    
    # 2. Get Data
    files = glob.glob("data/market_data/*.parquet")
    if not files:
        print("❌ No data found.")
        return

    results = []

    for f in files:
        asset = os.path.basename(f).replace("_processed.parquet", "")
        try:
            df = pd.read_parquet(f)
            # Normalize columns
            df.columns = [c.lower() for c in df.columns]
            
            if 'close' not in df.columns: continue
            
            prices = df['close']
            
            # 3. THE SIMULATION LOOP
            # We start with $1000
            capital = 1000.0
            position = 0.0
            entry_price = 0.0
            trades = 0
            
            # We need a rolling window, so we iterate through time
            # (Simplified vector backtest for speed)
            
            # Calculate signals for the whole dataframe at once? 
            # No, 'GodMode' needs a rolling window. We'll iterate.
            
            # Optimization: Calculate rolling metrics using Pandas first
            log_ret = np.log(prices / prices.shift(1))
            rolling_vol = log_ret.rolling(50).std()
            rolling_trend = log_ret.rolling(50).apply(lambda x: abs(x.autocorr(lag=1)))
            
            # Reconstruct the "Current D" metric efficiently
            # D = Volatility / (Range / Price)
            # This is complex to vectorise perfectly matching the class, 
            # but we will loop for accuracy.
            
            in_market = False
            equity_curve = []
            
            # We skip the first 50 candles (warmup)
            for i in range(50, len(df)):
                current_price = prices.iloc[i]
                price_slice = prices.iloc[i-50:i]
                
                # ASK THE PHYSICS ENGINE
                signal = engine.scan_market(price_slice)
                
                # EXECUTION LOGIC
                if signal == "GOD_MODE_ENGAGE" and not in_market:
                    # BUY
                    position = capital / current_price
                    capital = 0
                    entry_price = current_price
                    in_market = True
                    trades += 1
                
                elif (signal == "CRASH_PROTECTION" or signal == "WAIT") and in_market:
                    # SELL
                    capital = position * current_price
                    position = 0
                    in_market = False
                
                # Track Value
                current_val = capital if not in_market else position * current_price
                equity_curve.append(current_val)

            # Final Settlement
            final_value = capital if not in_market else position * prices.iloc[-1]
            buy_hold_return = ((prices.iloc[-1] - prices.iloc[50]) / prices.iloc[50]) * 100
            god_mode_return = ((final_value - 1000) / 1000) * 100
            
            print(f"📊 {asset}:")
            print(f"   -> Buy & Hold:   {buy_hold_return:+.2f}%")
            print(f"   -> God Mode:     {god_mode_return:+.2f}%")
            print(f"   -> Trades:       {trades}")
            if god_mode_return > buy_hold_return:
                print("   ✅ BEAT THE MARKET")
            else:
                print("   ❌ UNDERPERFORMED (Parameters might be too strict)")
            print("--------------------------------------")
            
        except Exception as e:
            print(f"⚠️ Error on {asset}: {e}")

if __name__ == "__main__":
    run_physics_backtest()
