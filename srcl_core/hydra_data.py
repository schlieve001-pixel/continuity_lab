"""
SRCL ELITE - DATA DOWNLOADER (Hydra Edition)
--------------------------------------------
Downloads BTC, ETH, SOL, BNB, ADA to ensure full market coverage.
"""
import yfinance as yf
import pandas as pd
import numpy as np
import os

DATA_DIR = "data/market_data"
os.makedirs(DATA_DIR, exist_ok=True)

TICKERS = ["BTC-USD", "ETH-USD", "SOL-USD", "BNB-USD", "ADA-USD"]

def process_ticker(ticker):
    print(f"📡 Downloading {ticker}...")
    df = yf.download(ticker, period="5y", interval="1d", auto_adjust=True, progress=False)
    
    # Flatten MultiIndex if necessary
    if isinstance(df.columns, pd.MultiIndex):
        try:
            df = df.xs(ticker, axis=1, level=1)
        except:
            pass # Fallback if structure is flat

    if df.empty:
        print(f"❌ Failed to download {ticker}")
        return

    # Quant Metrics
    df['Log_Returns'] = np.log(df['Close'] / df['Close'].shift(1))
    df['Volatility_20d'] = df['Log_Returns'].rolling(window=20).std() * np.sqrt(252)
    df['SMA_200'] = df['Close'].rolling(window=200).mean()
    # ATR Proxy
    df['ATR_Proxy'] = df['Close'] * df['Volatility_20d']
    
    df.dropna(inplace=True)
    
    save_path = f"{DATA_DIR}/{ticker}_processed.parquet"
    df.to_parquet(save_path)
    print(f"✅ Saved {ticker} ({len(df)} rows)")

if __name__ == "__main__":
    for t in TICKERS:
        process_ticker(t)
