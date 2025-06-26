# app.py

import streamlit as st
from main.automation import run_pipeline
from data.data_fetcher import fetch_stock_data
from core.strategy import generate_signals
from core.backtest import run_backtest
from core.ml_model import train_predict_model
from services.gsheet_logger import log_trades, log_summary
from services.telegram_alert import (
    send_pipeline_status,
    send_trade_alert,
    send_error_alert,
)

import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.metrics import confusion_matrix
import plotly.express as px

st.set_page_config(page_title="📊 Algo Trading Dashboard", layout="wide")

st.title("📈 Algo-Trading Dashboard (Strategy + ML + GSheet)")
symbols = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "SBIN.NS", "ITC.NS"]
symbol = st.selectbox("Choose Stock Symbol:", symbols)

if st.button("🚀 Run Algo"):
    with st.spinner(f"Running algo pipeline for {symbol}..."):
        try:
            send_pipeline_status("STARTED", symbol)

            # Fetch and preprocess
            df = fetch_stock_data(symbol, interval="1d", lookback="6mo")
            df = generate_signals(df)

            # Display raw data
            st.subheader("📅 Latest Data (w/ Indicators)")
            st.dataframe(df.tail(50), use_container_width=True)

            # Price Chart
            st.subheader("📈 Price + MA")
            fig = go.Figure()
            fig.add_trace(
                go.Scatter(
                    x=df["Date"], y=df["Close"], name="Close", line=dict(color="blue")
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=df["Date"],
                    y=df["MA_20"],
                    name="MA 20",
                    line=dict(color="green", dash="dot"),
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=df["Date"],
                    y=df["MA_50"],
                    name="MA 50",
                    line=dict(color="red", dash="dot"),
                )
            )
            st.plotly_chart(fig, use_container_width=True)

            st.subheader("📈 RSI")
            rsi_fig = go.Figure()
            rsi_fig.add_trace(
                go.Scatter(
                    x=df["Date"], y=df["RSI"], name="RSI", line=dict(color="orange")
                )
            )
            rsi_fig.add_hline(y=30, line_dash="dash", line_color="gray")
            rsi_fig.add_hline(y=70, line_dash="dash", line_color="gray")
            st.plotly_chart(rsi_fig, use_container_width=True)

            st.subheader("📈 Volume")
            vol_fig = px.area(df, x="Date", y="Volume", title="Volume Trend")
            st.plotly_chart(vol_fig, use_container_width=True)

            # Backtest & ML
            trades_df, stats = run_backtest(df)
            log_trades(trades_df, sheet_name=f"{symbol}_Trades")
            log_summary(stats, sheet_name=f"{symbol}_Summary")

            ml_result = train_predict_model(df)

            send_pipeline_status("COMPLETED", symbol)

        except Exception as e:
            send_error_alert(str(e))
            st.error(f"❌ Error occurred: {e}")

    st.success("✅ Algo Run Complete")

    st.subheader("📈 Strategy Backtest Summary")
    for k, v in stats.items():
        st.write(f"**{k}**: {v}")

    if not trades_df.empty:
        st.subheader("📌 Trade Details")
        st.dataframe(trades_df, use_container_width=True)
        st.write("**Buy/Sell Price Summary:**")
        st.write(
            trades_df[["Buy_Date", "Buy_Price", "Sell_Date", "Sell_Price"]].tail(10)
        )

        # Send Telegram alerts for trades
        for _, row in trades_df.iterrows():
            send_trade_alert(symbol, "BUY", row["Buy_Price"], str(row["Buy_Date"]))
            send_trade_alert(symbol, "SELL", row["Sell_Price"], str(row["Sell_Date"]))
    else:
        st.warning("No trades executed during this period.")

    st.subheader("📄 ML Training Data (Preview)")
    st.dataframe(ml_result["training_df"].tail(20), use_container_width=True)

    st.subheader("📊 ML Dataset EDA")
    st.plotly_chart(
        px.pie(ml_result["training_df"], names="Target", title="Target Distribution"),
        use_container_width=True,
    )
    st.plotly_chart(
        px.histogram(
            ml_result["training_df"],
            x="RSI",
            color="Target",
            nbins=30,
            title="RSI Histogram",
        ),
        use_container_width=True,
    )
    st.plotly_chart(
        px.scatter(
            ml_result["training_df"],
            x="MACD",
            y="MACD_Signal",
            color="Target",
            title="MACD vs Signal",
        ),
        use_container_width=True,
    )

    st.subheader("📋 ML Classification Report")
    st.write(f"**Next Day Prediction:** `{ml_result['next_day_prediction']}`")
    st.write(f"**Model Accuracy:** `{ml_result['accuracy']}%`")
    st.dataframe(ml_result["classification_report_df"], use_container_width=True)

    st.subheader("📌 Confusion Matrix")
    cm = ml_result["confusion_matrix"]
    fig_cm = px.imshow(
        cm,
        text_auto=True,
        title="Confusion Matrix",
        labels=dict(x="Predicted", y="Actual"),
        x=["DOWN", "UP"],
        y=["DOWN", "UP"],
    )
    st.plotly_chart(fig_cm, use_container_width=True)

    st.info("📤 Trade data & summary successfully uploaded to Google Sheets!")
    gsheet_url = f"https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID"
    st.markdown(f"🔗 [Open Google Sheet]({gsheet_url})")
