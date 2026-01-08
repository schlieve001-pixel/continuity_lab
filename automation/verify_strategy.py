"""
SRCL ELITE - STRATEGY VERIFIER (Dynamic ATR Edition)
----------------------------------------------------
Verifies the "Dynamic Multiplier" strategy.
Hardcoded with your latest AI results.
"""
import sys
import os
import pandas as pd
import numpy as np

# Ensure we can import from core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from srcl_core.backtest_engine import QuantEngine

# 🏆 YOUR LATEST "LAZY SNIPER" PARAMETERS
WINNING_PARAMS = {
  "w_trend": 0.8507506355636139,
  "w_mean_rev": 0.9730051065798693,
  "w_vol": 0.9763866068148888,
  "rsi_period": 30,             # <--- THE SUSPECT (Too slow?)
  "buy_thresh": 0.2049746439228379,
  "sell_thresh": 0.1283777554734966,
  "sl_multiplier": 2.1441633656419823, # Dynamic Stop (2.1x Volatility)
  "tp_multiplier": 4.400806252567385   # Dynamic Target (4.4x Volatility)
}

def print_audit_report(params):
    print("🚀 Initializing Dynamic Audit Engine...")
    engine = QuantEngine(ticker="BTC-USD")
    df = engine.data.copy()
    
    # --- REPLICATE LOGIC FROM BACKTEST ENGINE ---
    w_trend = params.get('w_trend', 0.5)
    w_mean_rev = params.get('w_mean_rev', 0.5)
    w_vol = params.get('w_vol', 0.5)
    rsi_period = int(params.get('rsi_period', 14))
    buy_thresh = params.get('buy_thresh', 0.2)
    sell_thresh = params.get('sell_thresh', 0.2)
    sl_multiplier = params.get('sl_multiplier', 2.0)
    tp_multiplier = params.get('tp_multiplier', 3.0)

    # Generate Signals
    sma_fast = df['Close'].rolling(window=20).mean()
    sma_slow = df['Close'].rolling(window=50).mean()
    trend_signal = np.where(sma_fast > sma_slow, 1.0, -1.0)

    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=rsi_period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=rsi_period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    rsi_signal = (50 - rsi) / 50 

    vol_signal = np.where(df['Volatility_20d'] > 0.03, -1.0, 1.0)
    raw_score = (w_trend * trend_signal) + (w_mean_rev * rsi_signal) + (w_vol * vol_signal)

    # Execution Loop
    prices = df['Close'].values
    atrs = df['ATR_Proxy'].values
    signals = raw_score.values
    dates = df.index
    
    balance = 1000.0
    position = 0
    entry_price = 0.0
    stop_price = 0.0
    target_price = 0.0
    
    trades = []
    equity_curve = []
    
    for i in range(len(prices)):
        price = prices[i]
        signal = signals[i]
        date = dates[i]
        current_atr = atrs[i]
        
        current_val = balance
        
        if position == 1:
            # Check Exits
            pnl = (price - entry_price) / entry_price
            
            # Stop Loss (Dynamic)
            if price < stop_price:
                balance = balance * (stop_price / entry_price) # Exit exactly at stop
                position = 0
                trades.append({'date': date, 'type': 'STOP_LOSS', 'pnl': (stop_price - entry_price)/entry_price})
            # Take Profit (Dynamic)
            elif price > target_price:
                balance = balance * (target_price / entry_price) # Exit exactly at target
                position = 0
                trades.append({'date': date, 'type': 'TAKE_PROFIT', 'pnl': (target_price - entry_price)/entry_price})
            # Signal Exit
            elif signal < -sell_thresh:
                balance = balance * (1 + pnl)
                position = 0
                trades.append({'date': date, 'type': 'SIGNAL_EXIT', 'pnl': pnl})
            else:
                current_val = balance * (1 + pnl)
                
        elif position == 0:
            if signal > buy_thresh:
                position = 1
                entry_price = price
                # Set Barriers at Entry
                stop_dist = current_atr * sl_multiplier
                target_dist = current_atr * tp_multiplier
                stop_price = entry_price - stop_dist
                target_price = entry_price + target_dist
                
                trades.append({'date': date, 'type': 'ENTRY', 'pnl': 0})
        
        equity_curve.append(current_val)

    # --- REPORTING ---
    equity_series = pd.Series(equity_curve)
    total_return = (equity_series.iloc[-1] - 1000.0) / 1000.0 * 100
    
    peak = equity_series.cummax()
    drawdown = (equity_series - peak) / peak
    max_drawdown = drawdown.min() * 100
    
    # Win Rate
    completed_trades = [t for t in trades if t['type'] != 'ENTRY']
    winning_trades = [t for t in completed_trades if t['pnl'] > 0]
    win_rate = (len(winning_trades) / len(completed_trades)) * 100 if len(completed_trades) > 0 else 0

    print("\n📊 SRCL DYNAMIC STRATEGY AUDIT")
    print("=" * 40)
    print(f"💰 Starting Balance: $1,000.00")
    print(f"🏁 Final Balance:    ${equity_series.iloc[-1]:,.2f}")
    print(f"📈 Total Return:     {total_return:.2f}%")
    print(f"📉 Max Drawdown:     {max_drawdown:.2f}%")
    print(f"🎯 Win Rate:         {win_rate:.2f}%")
    print(f"🔄 Total Trades:     {len(completed_trades)}")
    print("=" * 40)
    print("Parameters Used:")
    print(f"RSI Period: {params['rsi_period']}")
    print(f"Stop Multiplier: {params['sl_multiplier']:.2f}x ATR")
    print(f"Target Multiplier: {params['tp_multiplier']:.2f}x ATR")

if __name__ == "__main__":
    print_audit_report(WINNING_PARAMS)
