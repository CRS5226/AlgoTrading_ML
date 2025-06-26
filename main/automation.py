# automation.py

from data.data_fetcher import fetch_stock_data
from core.strategy import generate_signals
from core.backtest import run_backtest
from core.ml_model import train_predict_model
from services.gsheet_logger import log_trades, log_summary

def run_pipeline(symbol: str, interval="1d", lookback="6mo"):
    print(f"\n🔁 Running pipeline for: {symbol}")

    # Fetch & process data
    df = fetch_stock_data(symbol, interval=interval, lookback=lookback)
    df = generate_signals(df)

    # Backtest
    trades_df, stats = run_backtest(df)

    # Log to GSheet
    log_trades(trades_df, sheet_name=f"{symbol}_Trades")
    log_summary(stats, sheet_name=f"{symbol}_Summary")

    # ML Prediction
    ml_result = train_predict_model(df)
    print(
        f"📈 Accuracy: {ml_result['accuracy']}% | 📊 Next day: {ml_result['next_day_prediction']}"
    )

    return stats, ml_result
