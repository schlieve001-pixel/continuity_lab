"""
SRCL ELITE - LIVE SIGNAL GENERATOR
----------------------------------
1. Downloads latest Candle (Today).
2. Loads your WINNING HYDRA PARAMETERS.
3. Prints clear BUY/SELL instructions for BTC & ETH.
"""
import yfinance as yf
import pandas as pd
import numpy as np
import json
import os
import sys
from datetime import datetime

# 🏆 LOAD THE HYDRA WINNER
PARAM_FILE = "automation/best_hydra_params.json"

if not os.path.exists(PARAM_FILE):
    print("🚨 ERROR: No strategy found. Run hydra_optimizer.py first.")
    sys.exit()

with open(PARAM_FILE, 'r') as f:
    PARAMS = json.load(f)

ASSETS = ["BTC-USD", "ETH-USD"]

def get_live_signal(ticker):
    print(f"\n📡 ANALYZING {ticker}...")
    
    # Get enough data to calculate 200 SMA and RSI
    df = yf.download(ticker, period="1y", interval="1d", progress=False)
    
    if isinstance(df.columns, pd.MultiIndex):
        df = df.xs(ticker, axis=1, level=1)
    
    # --- CALCULATE INDICATORS ---
    # 1. 200 SMA (Regime Filter)
    df['SMA_200'] = df['Close'].rolling(window=200).mean()
    
    # 2. RSI (Signal)
    period = int(PARAMS['rsi_period'])
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    # 3. Volatility (ATR)
    df['Log_Ret'] = np.log(df['Close'] / df['Close'].shift(1))
    df['Vol_20'] = df['Log_Ret'].rolling(window=20).std() * np.sqrt(252)
    df['ATR_Proxy'] = df['Close'] * df['Vol_20']
    
    # --- GET LATEST VALUES ---
    latest = df.iloc[-1]
    price = latest['Close']
    sma = latest['SMA_200']
    current_rsi = latest.iloc[-1] # RSI column index is complex, simplified here:
    
    # Re-calc RSI specifically for last row to be safe
    current_rsi = rsi.iloc[-1]
    current_atr = latest['ATR_Proxy']
    
    # --- LOGIC CORE ---
    is_bull_regime = price > sma
    
    # Normalize RSI Signal (Same as Backtester)
    # 50 = 0.0, 30 = 0.4, 70 = -0.4
    rsi_signal = (50 - current_rsi) / 50 
    
    # Trend Signal
    # We approximate trend signal based on price vs sma for live readout
    trend_signal = 1.0 if is_bull_regime else -1.0
    
    # Vol Signal
    vol_signal = 1.0 if latest['Vol_20'] < 0.04 else -1.0
    
    # FINAL SCORE
    raw_score = (PARAMS['w_trend'] * trend_signal) + \
                (PARAMS['w_mean_rev'] * rsi_signal) + \
                (PARAMS['w_vol'] * vol_signal)
    
    # --- DECISION ---
    buy_thresh = PARAMS['buy_thresh']
    sell_thresh = PARAMS['sell_thresh']
    
    print(f"   🔹 Price:      ${price:,.2f}")
    print(f"   🔹 Regime:     {'🟢 BULL (Summer)' if is_bull_regime else '🔴 BEAR (Winter)'}")
    print(f"   🔹 RSI ({period}):   {current_rsi:.1f}")
    print(f"   🔹 Signal Strength: {raw_score:.3f} (Need > {buy_thresh:.3f})")
    
    # LOGIC CHECK
    if raw_score > buy_thresh:
        # Check Bear Market Filter
        if not is_bull_regime and raw_score < 0.3:
            print("   ⚠️  SIGNAL IGNORED: Weak Buy Signal in Bear Market.")
            return
            
        print("   🚀 ACTION: >> BUY NOW <<")
        
        # Calculate Risk Levels
        stop_loss = price - (current_atr * PARAMS['sl_multiplier'])
        take_profit = price + (current_atr * PARAMS['tp_multiplier'])
        
        print(f"      🛡️ STOP LOSS:   ${stop_loss:,.2f}")
        print(f"      🎯 TARGET:      ${take_profit:,.2f}")
        print(f"      ⚖️ R:R RATIO:   1 : {PARAMS['tp_multiplier']/PARAMS['sl_multiplier']:.2f}")
        
    elif raw_score < -sell_thresh:
        print("   🔻 ACTION: >> SELL / CLOSE <<")
    else:
        print("   💤 ACTION: HOLD / CASH (No Signal)")

if __name__ == "__main__":
    print(f"🔮 SRCL LIVE SIGNAL DECODER ({datetime.now().strftime('%Y-%m-%d %H:%M')})")
    print("=" * 60)
    for asset in ASSETS:
        try:
            get_live_signal(asset)
        except Exception as e:
            print(f"Error analyzing {asset}: {e}")
    print("=" * 60)
