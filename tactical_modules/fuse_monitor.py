import numpy as np
import pandas as pd
import yfinance as yf

class StickyFuse:
    """
    THE TETHER TRACKER
    Monitors the correlation distance between Leader (COIN) and Follower (SOL).
    """
    def __init__(self, leader="COIN", follower="SOL-USD"):
        self.leader = leader
        self.follower = follower
        self.lookback = 30 # Days to calculate normal correlation

    def check_fuse(self):
        """
        Calculates if the rubber band is 'Normal', 'Stretched', or 'Snapped'.
        """
        # 1. GET DATA (Syncing dates)
        data = yf.download([self.leader, self.follower], period="3mo", interval="1d", progress=False, auto_adjust=True)['Close']
        
        # Drop rows where either is missing
        data = data.dropna()
        
        # 2. CALCULATE RELATIVE PERFORMANCE (Normalized to 0 start)
        # We look at the last 10 days specifically for the "Fuse" tension
        recent = data.tail(10).copy()
        
        # Normalize both to percentage change from 10 days ago
        leader_ret = (recent[self.leader] - recent[self.leader].iloc[0]) / recent[self.leader].iloc[0]
        follower_ret = (recent[self.follower] - recent[self.follower].iloc[0]) / recent[self.follower].iloc[0]
        
        # 3. CALCULATE THE SPREAD (The Distance)
        spread = abs(follower_ret.iloc[-1] - leader_ret.iloc[-1])
        correlation = recent[self.leader].corr(recent[self.follower])
        
        # 4. DEFINE STATUS
        # If Correlation drops below 0.5, the fuse is fraying.
        # If Spread > 5% (0.05), the rubber band is stretched.
        
        status = "✅ IN SYNC"
        action = "MONITOR"
        
        if correlation < 0.5:
            status = "⚠️ DECOUPLED (Core Broken)"
            action = "CAUTION"
            
        if spread > 0.08: # 8% Divergence
            status = "🚫 FUSE BROKEN (Extreme Spread)"
            action = "DO NOT CHASE"
            
        return {
            "spread_pct": spread * 100,
            "correlation": correlation,
            "leader_perf": leader_ret.iloc[-1] * 100,
            "follower_perf": follower_ret.iloc[-1] * 100,
            "status": status,
            "action": action
        }

if __name__ == "__main__":
    # SELF-DIAGNOSTIC
    fuse = StickyFuse()
    report = fuse.check_fuse()
    print(f"\n🔗 TETHER DIAGNOSTIC: {fuse.leader} vs {fuse.follower}")
    print(f"   Spread Gap:   {report['spread_pct']:.2f}%")
    print(f"   Correlation:  {report['correlation']:.2f}")
    print(f"   STATUS:       {report['status']}")
    print(f"   COMMAND:      {report['action']}")
