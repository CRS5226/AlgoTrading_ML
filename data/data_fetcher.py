# data/data_fetcher.py

import pandas as pd
import yfinance as yf
from config.config import DEFAULT_LOOKBACK, DEFAULT_INTERVAL


def fetch_stock_data(
    symbol: str, interval: str = DEFAULT_INTERVAL, lookback: str = DEFAULT_LOOKBACK
):
    """
    Fetches historical stock data from Yahoo Finance.

    Parameters:
    - symbol (str): Stock ticker (e.g., "RELIANCE.NS")
    - interval (str): "1d" for daily, "15m" for intraday, etc.
    - lookback (str): Duration (e.g., "6mo", "1y")

    Returns:
    - DataFrame with OHLCV and Symbol columns
    """
    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(period=lookback, interval=interval)
        if df.empty:
            raise ValueError("Received empty dataframe from yfinance.")
        df = df.reset_index()
        df["Symbol"] = symbol
        return df
    except Exception as e:
        print(f"[ERROR] Failed to fetch data for {symbol}: {e}")
        return None
