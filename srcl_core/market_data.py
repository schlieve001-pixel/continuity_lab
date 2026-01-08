"""
SRCL ELITE - Market Data Ingestion Engine (Phase 1)
---------------------------------------------------
Pulls OHLCV data, cleans it, calculates volatility metrics,
and stores it in high-performance Parquet format.
"""

import yfinance as yf
import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

DATA_DIR = "data/market_data"
os.makedirs(DATA_DIR, exist_ok=True)

class MarketDataEngine:
    def __init__(self, tickers=None):
        self.tickers = tickers if tickers else ["SPY", "QQQ", "BTC-USD", "NVDA", "GLD"]
        self.period = "5y"  # 5 years of training data
        self.interval = "1d" # Daily candles (Start here, move to 1h later)

    def fetch_data(self):
        """Pulls raw data from Yahoo Finance."""
        print(f"📡 Connecting to Global Markets... Pulling: {self.tickers}")
        
        # Download in bulk for speed
        raw_data = yf.download(
            tickers=self.tickers, 
            period=self.period, 
            interval=self.interval, 
            group_by='ticker',
            auto_adjust=True,
            threads=True
        )
        
        return raw_data

    def process_ticker(self, ticker, df):
        """Cleans and adds base Quant metrics to a single ticker."""
        if df.empty:
            return None
            
        df = df.copy()
        
        # 1. Basic Cleaning
        df.dropna(inplace=True)
        
        # 2. Add 'Returns' (The heartbeat of Quant)
        df['Log_Returns'] = np.log(df['Close'] / df['Close'].shift(1))
        
        # 3. Add Volatility (Risk) - Annualized
        df['Volatility_20d'] = df['Log_Returns'].rolling(window=20).std() * np.sqrt(252)
        
        # 4. Add Regime Indicator (Simple Trend)
        df['SMA_50'] = df['Close'].rolling(window=50).mean()
        df['SMA_200'] = df['Close'].rolling(window=200).mean()
        df['Regime'] = np.where(df['SMA_50'] > df['SMA_200'], 1, -1) # 1 = Bull, -1 = Bear
        
        # Drop NaN created by rolling windows
        df.dropna(inplace=True)
        
        return df

    def run_pipeline(self):
        """Executes the full extraction and save process."""
        data = self.fetch_data()
        
        for ticker in self.tickers:
            try:
                # Handle yfinance multi-index format
                if len(self.tickers) > 1:
                    ticker_df = data[ticker]
                else:
                    ticker_df = data
                
                processed_df = self.process_ticker(ticker, ticker_df)
                
                if processed_df is not None:
                    # Save as Parquet (Fast & Professional)
                    filename = f"{DATA_DIR}/{ticker}_processed.parquet"
                    processed_df.to_parquet(filename)
                    print(f"✅ {ticker}: Processed & Saved ({len(processed_df)} rows)")
                else:
                    print(f"⚠️ {ticker}: No data found.")
                    
            except Exception as e:
                print(f"❌ Error processing {ticker}: {e}")

if __name__ == "__main__":
    engine = MarketDataEngine()
    engine.run_pipeline()
