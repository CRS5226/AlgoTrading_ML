# core/strategy.py

import pandas as pd


def calculate_rsi(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """Calculate the Relative Strength Index (RSI)."""
    delta = df["Close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window=period, min_periods=period).mean()
    avg_loss = loss.rolling(window=period, min_periods=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi


def calculate_moving_averages(df: pd.DataFrame, short: int = 20, long: int = 50):
    """Calculate 20-DMA and 50-DMA and add them to the dataframe."""
    df['MA_20'] = df['Close'].rolling(window=short, min_periods=1).mean()
    df['MA_50'] = df['Close'].rolling(window=long, min_periods=1).mean()
    return df


def generate_signals(df: pd.DataFrame) -> pd.DataFrame:
    """Generate Buy/Sell signals based on RSI and MA crossover."""
    df = df.copy()

    df["RSI"] = calculate_rsi(df)
    df = calculate_moving_averages(df)

    # Define Buy and Sell Conditions
    df["Buy_Signal"] = (df["RSI"] < 30) & (df["MA_20"] > df["MA_50"])
    df["Sell_Signal"] = df["RSI"] > 70

    return df
