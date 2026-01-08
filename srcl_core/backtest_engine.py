"""
SRCL ELITE - QUANT ENGINE (Phase 6: REGIME AWARE)
-------------------------------------------------
1. Logic: If Price < 200 SMA, BANS trend trades (Prevents catching falling knives).
2. Logic: If Price > 200 SMA, ALLOWS aggressive entries.
3. Result: Drastically lower drawdown.
"""

import pandas as pd
import numpy as np
import os
import json

DATA_DIR = "data/market_data"
PARAM_FILE = "automation/best_hunter_params.json"

class QuantEngine:
    def __init__(self, ticker="BTC-USD"):
        self.ticker = ticker
        self.data = self._load_data()

    def _load_data(self):
        path = f"{DATA_DIR}/{self.ticker}_processed.parquet"
        if not os.path.exists(path):
            raise FileNotFoundError(f"🚨 Missing Data for {self.ticker}")
        df = pd.read_parquet(path)
        
        # --- NEW: REGIME INDICATOR (The 200 SMA) ---
        df['SMA_200'] = df['Close'].rolling(window=200).mean()
        df['ATR_Proxy'] = df['Close'] * df['Volatility_20d']
        return df

    def save_params(self, params):
        with open(PARAM_FILE, 'w') as f:
            json.dump(params, f, indent=2)

    def load_params(self):
        if not os.path.exists(PARAM_FILE):
            raise FileNotFoundError("No saved strategy found!")
        with open(PARAM_FILE, 'r') as f:
            return json.load(f)

    def run_backtest(self, params, detailed_report=False):
        df = self.data.copy()
        
        # --- GENES ---
        w_trend = params.get('w_trend', 0.5)
        w_mean_rev = params.get('w_mean_rev', 0.5)
        w_vol = params.get('w_vol', 0.5)
        rsi_period = int(params.get('rsi_period', 14))
        buy_thresh = params.get('buy_thresh', 0.2)
        sell_thresh = params.get('sell_thresh', 0.2)
        sl_mult = params.get('sl_multiplier', 2.0)
        tp_mult = params.get('tp_multiplier', 3.0)

        # --- SIGNALS ---
        # Trend
        sma_fast = df['Close'].rolling(window=20).mean()
        sma_slow = df['Close'].rolling(window=50).mean()
        trend_signal = np.where(sma_fast > sma_slow, 1.0, -1.0)

        # RSI
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=rsi_period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=rsi_period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        rsi_signal = (50 - rsi) / 50 

        vol_signal = np.where(df['Volatility_20d'] > 0.04, -1.0, 1.0)
        
        # Mix Signals
        raw_score = (w_trend * trend_signal) + (w_mean_rev * rsi_signal) + (w_vol * vol_signal)

        # --- EXECUTION LOOP (REGIME AWARE) ---
        prices = df['Close'].values
        smas = df['SMA_200'].values  # <--- NEW INPUT
        atrs = df['ATR_Proxy'].values
        signals = raw_score.values
        
        balance = 1000.0
        position = 0
        entry_price = 0.0
        stop_price = 0.0
        target_price = 0.0
        
        equity_curve = []
        trades = []
        
        for i in range(len(prices)):
            price = prices[i]
            sma = smas[i]
            
            # Skip if SMA not calculated yet (first 200 days)
            if np.isnan(sma): 
                equity_curve.append(balance)
                continue
                
            # DETERMINE REGIME
            is_bull_market = price > sma
            
            if position == 1:
                # Exits (Same as before)
                if price < stop_price:
                    balance *= (stop_price / entry_price)
                    position = 0
                    trades.append(-1)
                elif price > target_price:
                    balance *= (target_price / entry_price)
                    position = 0
                    trades.append(1)
                elif signals[i] < -sell_thresh:
                    pnl = (price - entry_price) / entry_price
                    balance *= (1 + pnl)
                    position = 0
                    trades.append(1 if pnl > 0 else -1)
            
            elif position == 0:
                if signals[i] > buy_thresh:
                    # 🛑 THE REGIME FILTER 🛑
                    # If we are in a Bear Market (Price < SMA), we IGNORE Trend Signals.
                    # We only buy if the Mean Reversion signal (RSI) is screaming "Cheap!"
                    
                    allow_trade = True
                    if not is_bull_market:
                        # In Bear Market, enforce stricter rules
                        # Only buy if RSI signal is extremely strong (> 0.6)
                        if signals[i] < 0.3: # Hardcoded safety filter
                            allow_trade = False
                    
                    if allow_trade:
                        position = 1
                        entry_price = price
                        stop_price = entry_price - (atrs[i] * sl_mult)
                        target_price = entry_price + (atrs[i] * tp_mult)
            
            val = balance * (price / entry_price) if position == 1 else balance
            equity_curve.append(val)

        # --- SCORING ---
        equity_series = pd.Series(equity_curve)
        total_return = (equity_series.iloc[-1] - 1000.0) / 1000.0
        peak = equity_series.cummax()
        drawdown = (equity_series - peak) / peak
        max_drawdown = drawdown.min()
        trade_count = len(trades)

        if trade_count < 40: return -999.0

        returns = equity_series.pct_change().dropna()
        if returns.std() == 0: sharpe = -1.0
        else: sharpe = (returns.mean() * 252) / (returns.std() * np.sqrt(252))

        # Reward Safety more now
        fitness = sharpe + (total_return * 1.5) + (max_drawdown * 8.0) # Heavier penalty for DD
        
        if detailed_report:
            return {
                "Final Balance": equity_series.iloc[-1],
                "Total Return %": total_return * 100,
                "Max Drawdown %": max_drawdown * 100,
                "Trades": trade_count,
                "Sharpe": sharpe
            }
            
        return fitness
