import sys
import os
import time
import pandas as pd
from datetime import datetime

# FIX IMPORTS
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from physics_engine.chaos_metrics import ChaosEngine
from tactical_modules.fuse_monitor import StickyFuse
from command_center.fusion_reactor import FusionReactor

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def log_to_blackbox(fuse_data, physics_data):
    """
    Saves the scan data to a CSV file for permanent record.
    """
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        
    filename = f"{log_dir}/market_blackbox.csv"
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Prepare the row
    record = {
        "timestamp": now,
        "leader": fuse_data.get('leader', 'N/A'),
        "follower": fuse_data.get('follower', 'N/A'),
        "gap_pct": fuse_data.get('spread_pct', 0),
        "correlation": fuse_data.get('correlation', 0),
        "fuse_status": fuse_data.get('status', 'UNKNOWN'),
        "action": fuse_data.get('action', 'WAIT')
    }
    
    # Add physics data (Force/Score) for the Follower if available
    # We flatten the physics report for the log
    if physics_data:
        # Assuming physics_data is a dict of results, we grab the Follower's stats
        # For simplicity in this V1 logger, we just log the Action
        pass

    # Convert to DataFrame and Append
    df = pd.DataFrame([record])
    
    # Write header only if file doesn't exist
    if not os.path.exists(filename):
        df.to_csv(filename, index=False)
    else:
        df.to_csv(filename, mode='a', header=False, index=False)

def main():
    reactor = FusionReactor()
    fuse = StickyFuse()
    
    print("⏳ INITIALIZING SYSTEMS... (Gathering 6mo Data)")
    
    while True:
        try:
            # 1. CALCULATE DATA
            fuse_data = fuse.check_fuse()
            
            # 2. LOG IT (The Black Box)
            log_to_blackbox(fuse_data, None)
            
            # 3. CLEAR SCREEN & RENDER UI
            clear_screen()
            now = datetime.now().strftime("%H:%M:%S")
            
            print(f"📡 STICKY FUSE MONITOR | UPDATED: {now}")
            print("=" * 70)
            print(f"LEADER     | {fuse.leader:<8} | REF        | ---            | 🏛️  INSTITUTIONAL")
            print(f"FOLLOWER   | {fuse.follower:<8} | GAP: {fuse_data['spread_pct']:.2f}% | CORR: {fuse_data['correlation']:.2f}   | 🚀 RETAIL FLOW")
            print("=" * 70)
            
            # STATUS LOGIC
            status_icon = "⚪"
            if "BROKEN" in fuse_data['status']:
                status_icon = "⛔"
            elif "DECOUPLED" in fuse_data['status']:
                status_icon = "⚠️"
            elif "SYNC" in fuse_data['status']:
                status_icon = "✅"

            print(f"📢 STATUS: {status_icon} {fuse_data['status']}")
            print(f"⚡ ACTION: {fuse_data['action']}")
            print("-" * 70)
            
            # 4. DRAW PHYSICS LOG
            print("📜 PHYSICS LOG (LATEST SCAN):")
            reactor.scan_market()
            
            print(f"\n[💾 LOG SAVED TO logs/market_blackbox.csv]")
            print("(Press Ctrl+C to Stop | Refreshing in 60s)")
            
            time.sleep(60)
            
        except KeyboardInterrupt:
            print("\n🛑 MONITOR STOPPED.")
            break
        except Exception as e:
            print(f"CRITICAL ERROR: {e}")
            time.sleep(10)

if __name__ == "__main__":
    main()
