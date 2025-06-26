from data.data_fetcher import fetch_stock_data
from core.strategy import generate_signals
from core.backtest import run_backtest
from services.gsheet_logger import log_trades, log_summary

df = fetch_stock_data("RELIANCE.NS")
df = generate_signals(df)
trades_df, stats = run_backtest(df)

log_trades(trades_df, sheet_name="Reliance_Trades")
log_summary(stats, sheet_name="Reliance_Summary")
