import pandas as pd


def run_backtest(df: pd.DataFrame, initial_capital: float = 100000):
    """
    Runs a simple backtest on the signal DataFrame.

    Assumptions:
    - Buy when Buy_Signal is True
    - Sell when Sell_Signal is True or at the end
    - All-in trade (no partial capital)

    Returns:
    - trades_df: Trade log with entry/exit
    - stats: P&L summary
    """
    df = df.copy()
    trades = []
    position = None

    for i in range(len(df)):
        row = df.iloc[i]

        if position is None and row["Buy_Signal"]:
            # Enter trade
            position = {
                "Buy_Date": row["Date"],
                "Buy_Price": row["Close"],
                "Buy_Index": i,
            }

        elif position and (row["Sell_Signal"] or i == len(df) - 1):
            # Exit trade
            position["Sell_Date"] = row["Date"]
            position["Sell_Price"] = row["Close"]
            position["Sell_Index"] = i
            position["PnL"] = row["Close"] - position["Buy_Price"]
            position["Return_%"] = (
                (row["Close"] - position["Buy_Price"]) / position["Buy_Price"]
            ) * 100
            trades.append(position)
            position = None

    trades_df = pd.DataFrame(trades)

    # Initialize total_pnl
    total_pnl = 0.0

    if trades_df.empty:
        stats = {
            "Total Trades": 0,
            "Winning Trades": 0,
            "Win Ratio (%)": 0.0,
            "Total PnL": total_pnl,
            "Cumulative Return (%)": 0.0,
        }
    else:
        total_pnl = trades_df["PnL"].sum()
        win_trades = trades_df[trades_df["PnL"] > 0].shape[0]
        total_trades = trades_df.shape[0]
        win_ratio = (win_trades / total_trades) * 100
        cumulative_return = (total_pnl / initial_capital) * 100

        stats = {
            "Total Trades": total_trades,
            "Winning Trades": win_trades,
            "Win Ratio (%)": round(win_ratio, 2),
            "Total PnL": round(total_pnl, 2),
            "Cumulative Return (%)": round(cumulative_return, 2),
        }

    return trades_df, stats
