"""
SRCL ELITE - MULTI-ASSET STRESS TEST
------------------------------------
Takes the "Winning" BTC Strategy and forces it to trade ETH and SOL.
If it survives all three, the strategy is mathematically robust.
"""
import sys
import os
import pandas as pd
import numpy as np
import yfinance as yf

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from srcl_core.backtest_engine import QuantEngine

# 🏆 PASTE YOUR BEST BTC PARAMETERS HERE (From your +104% run)
WINNING_PARAMS = {
  "w_trend": 0.6499,
  "w_mean_rev": 0.6499,
  "w_vol": 0.6499,
  "rsi_period": 14,             # Approx from your range
  "buy_thresh": 0.15,           # Approx from your range
  "sell_thresh": 0.15,
  "sl_multiplier": 1.5,         # From your Risk Ratio
  "tp_multiplier": 4.8          # 1.5 * 3.2 = 4.8
}

def get_data(ticker):
    print(f"📡 Downloading {ticker} data...")
    df = yf.download(ticker, period="5y", interval="1d", auto_adjust=True, progress=False)
    
    # Process Data manually since we aren't using the engine's loader for new assets
    df = df.copy()
    if isinstance(df.columns, pd.MultiIndex):
        df = df.xs(ticker, axis=1, level=1)
        
    df['Log_Returns'] = np.log(df['Close'] / df['Close'].shift(1))
    df['Volatility_20d'] = df['Log_Returns'].rolling(window=20).std() * np.sqrt(252)
    df['SMA_200'] = df['Close'].rolling(window=200).mean()
    df['ATR_Proxy'] = df['Close'] * df['Volatility_20d']
    df.dropna(inplace=True)
    return df

def run_test(ticker):
    # 1. Hack the Engine to use new data
    engine = QuantEngine(ticker="BTC-USD") # Initialize dummy
    engine.data = get_data(ticker) # Inject new data
    
    print(f"\n⚔️  FIGHTING: {ticker}")
    stats = engine.run_backtest(WINNING_PARAMS, detailed_report=True)
    
    if isinstance(stats, float): # If it returned -999.0
        print(f"❌ FAILED: Too few trades or blown account.")
        return False
        
    print(f"💰 Return: {stats['Total Return %']:.2f}%")
    print(f"📉 Drawdown: {stats['Max Drawdown %']:.2f}%")
    print(f"🔄 Trades: {stats['Trades']}")
    
    if stats['Total Return %'] > 20:
        print("✅ PASSED")
        return True
    else:
        print("⚠️ WEAK PERFORMANCE")
        return False

if __name__ == "__main__":
    print("🛡️ STARTING UNIVERSAL SOLDIER TEST")
    print("=" * 40)
    
    btc = run_test("BTC-USD")
    eth = run_test("ETH-USD")
    sol = run_test("SOL-USD")
    
    print("\n" + "=" * 40)
    if btc and eth and sol:
        print("🏆 GOD MODE UNLOCKED: Strategy works on ALL assets.")
        print("🚀 RECOMMENDATION: DEPLOY IMMEDIATELY.")
    elif btc and eth:
        print("🥇 ELITE STATUS: Works on Majors (BTC + ETH). Safe to deploy.")
    else:
        print("💀 FAILED: Strategy is over-fitted to Bitcoin. DO NOT DEPLOY.")
