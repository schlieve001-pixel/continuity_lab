import numpy as np
import pandas as pd

class ChaosEngine:
    """
    THE SINGULARITY DETECTOR (V3: ROBUST ALIGNMENT)
    Fixes the '0.00 Force' bug by aligning Price and Volume dates.
    """
    
    def __init__(self):
        self.SINGULARITY_THRESHOLD = 150
        self.FORCE_THRESHOLD = 50 

    def analyze_physics(self, price_series, volume_series):
        # 1. DATA ALIGNMENT (The Fix)
        # Create a single dataframe to ensure dates match perfectly
        df = pd.DataFrame({'price': price_series, 'volume': volume_series})
        df = df.dropna() # Drop any rows where either Price OR Volume is missing
        
        if len(df) < 20:
            return {"status": "INSUFFICIENT_DATA", "score": 0, "force": 0}

        # 2. KINEMATICS
        # Velocity = ln(Price_t / Price_t-1)
        df['velocity'] = np.log(df['price'] / df['price'].shift(1))
        
        # Acceleration = Velocity_t - Velocity_t-1
        df['acceleration'] = df['velocity'].diff()
        
        # 3. COMPRESSION SCORE
        # Calculate volatility on the 'velocity' column we just made
        volatility = df['velocity'].rolling(window=14).std().iloc[-1]
        epsilon = 1e-8
        singularity_score = 1 / (volatility + epsilon)

        # 4. FORCE CALCULATION (Mass * Accel)
        # Normalize volume (Relative Mass)
        df['norm_vol'] = df['volume'] / df['volume'].rolling(20).mean()
        
        # Get the latest valid values
        last_accel = df['acceleration'].iloc[-1]
        last_mass = df['norm_vol'].iloc[-1]
        
        # Force = |Acceleration| * Relative Mass * 1000 (Scaler)
        force = abs(last_accel) * last_mass * 1000

        # 5. STATUS LOGIC
        status = "⚪ NOISE"
        if singularity_score > self.SINGULARITY_THRESHOLD:
            status = "🔴 SINGULARITY (COMPRESSION)"
        elif force > self.FORCE_THRESHOLD and singularity_score > 50:
            status = "⚠️ HIGH TENSION (HIDDEN FORCE)"

        return {
            "singularity_score": singularity_score,
            "force": force,
            "status": status
        }
