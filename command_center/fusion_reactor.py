import yfinance as yf
import pandas as pd
import sys
import os

# Fix import path to find the Physics Engine
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from physics_engine.chaos_metrics import ChaosEngine

class FusionReactor:
    def __init__(self):
        self.chaos_engine = ChaosEngine()
        self.watchlist = ["BTC-USD", "SOL-USD", "NVDA", "COIN"]
        print("☢️  FUSION REACTOR ONLINE: LIVE FEED CONNECTED.")

    def scan_market(self):
        print(f"\n{'ASSET':<10} | {'SCORE':<10} | {'FORCE':<10} | {'STATUS'}")
        print("-" * 65)
        
        # FIX: Changed period from "1mo" to "6mo" to ensure Volume math has enough data
        try:
            data = yf.download(self.watchlist, period="6mo", interval="1d", progress=False, auto_adjust=True)
            
            for ticker in self.watchlist:
                try:
                    # Handle Multi-index columns from yfinance
                    if isinstance(data.columns, pd.MultiIndex):
                        prices = data['Close'][ticker]
                        volume = data['Volume'][ticker]
                    else:
                        prices = data['Close']
                        volume = data['Volume']

                    # RUN PHYSICS
                    report = self.chaos_engine.analyze_physics(prices, volume)
                    
                    # Format numbers nicely (and handle NaNs if they still appear)
                    score = report['singularity_score']
                    force = report['force']
                    
                    # Use 0.00 if force is still nan for some reason
                    force_display = 0.00 if pd.isna(force) else force
                    
                    print(f"{ticker:<10} | {score:<10.2f} | {force_display:<10.2f} | {report['status']}")
                    
                except Exception as inner_e:
                    print(f"{ticker:<10} | ERROR      | 0.00       | {str(inner_e)[:20]}")
        
        except Exception as e:
            print(f"CRITICAL DATA ERROR: {e}")

if __name__ == "__main__":
    reactor = FusionReactor()
    reactor.scan_market()
