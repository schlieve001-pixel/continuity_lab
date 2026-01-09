import json

# THE FREE-TIER WAR ROOM
notebook_content = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# 🏛️ SRCL GOD MODE: FREE TIER PROTOCOL\n",
    "**Status:** Operational | **Cost:** $0.00\n",
    "\n",
    "This notebook runs the 'Singularity Physics Engine' using standard CPU power.\n",
    "It allows us to validate the strategy on live markets without burning Cloud Credits."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 1. INSTALL LIGHTWEIGHT LIBRARIES\n",
    "!pip install -q yfinance pandas numpy scipy matplotlib"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 2. THE GOD MODE PHYSICS ENGINE (Recovered DNA: Alpha 0.517)\n",
    "import numpy as np\n",
    "import pandas as pd\n",
    "from scipy.stats import entropy\n",
    "\n",
    "class GodMode:\n",
    "    def __init__(self):\n",
    "        # THE SINGULARITY CONSTANTS\n",
    "        self.ALPHA = 0.5165557212010854\n",
    "        self.BETA  = 0.8809978396320239\n",
    "        self.GAMMA = 0.7108258327150544\n",
    "        self.D     = 0.0904207499757942\n",
    "\n",
    "    def scan(self, prices):\n",
    "        if len(prices) < 50: return \"WAIT\"\n",
    "        \n",
    "        # 1. Physics Calculations\n",
    "        log_ret = np.log(prices / prices.shift(1)).dropna()\n",
    "        volatility = log_ret.std()\n",
    "        \n",
    "        # Fractal Dimension Proxy (Vol / Range)\n",
    "        range_size = prices.max() - prices.min()\n",
    "        if range_size == 0: return \"WAIT\"\n",
    "        current_D = volatility / (range_size / prices.iloc[-1])\n",
    "        \n",
    "        # Trend Coherence (Autocorrelation)\n",
    "        trend_strength = abs(log_ret.autocorr(lag=1))\n",
    "        \n",
    "        # 2. The Decision Matrix\n",
    "        # Matches the -412 Entropy Event Logic\n",
    "        if (current_D < 0.2) and (trend_strength > 0.5):\n",
    "            return \"🟢 ENGAGE (GOD MODE)\"\n",
    "        elif volatility > self.ALPHA:\n",
    "            return \"🔴 CRASH RISK (HIGH ENTROPY)\"\n",
    "        else:\n",
    "            return \"⚪ WAIT (NOISE)\""
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 3. LIVE MARKET SCAN (Free Data Feed)\n",
    "import yfinance as yf\n",
    "import matplotlib.pyplot as plt\n",
    "\n",
    "# Define Assets to Scan\n",
    "tickers = ['BTC-USD', 'ETH-USD', 'SOL-USD', 'BNB-USD', 'ADA-USD', 'NVDA', 'SPY', 'QQQ', 'MSTR', 'COIN']\n",
    "print(f\"📡 SCANNING {len(tickers)} ASSETS FOR SINGULARITY STRUCTURES...\\n\")\n",
    "\n",
    "data = yf.download(tickers, period=\"1y\", progress=False)['Close']\n",
    "engine = GodMode()\n",
    "\n",
    "for ticker in tickers:\n",
    "    try:\n",
    "        prices = data[ticker].dropna()\n",
    "        signal = engine.scan(prices)\n",
    "        \n",
    "        # Visual Output\n",
    "        print(f\"📊 {ticker.ljust(8)} | Signal: {signal}\")\n",
    "        \n",
    "    except Exception as e:\n",
    "        print(f\"⚠️ Error scanning {ticker}: {e}\")"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.10.12"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}

with open("SRCL_God_Mode_Free.ipynb", "w") as f:
    json.dump(notebook_content, f, indent=2)

print("✅ GENERATED: SRCL_God_Mode_Free.ipynb")
