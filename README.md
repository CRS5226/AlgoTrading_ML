# 📊 Algo Trading Prototype

A modular, end-to-end algo trading pipeline with:
- Automated data fetching (Yahoo Finance)
- Technical signal generation & backtesting
- Machine Learning prediction
- Google Sheets logging
- Telegram alerts
- Interactive Streamlit dashboard

---

## 🚀 Features

- **Data Source:** Yahoo Finance via `yfinance`
- **Strategy:** RSI + Moving Average crossover
- **Backtesting:** Simple buy/sell logic with P&L stats
- **ML Model:** Logistic Regression (predicts next-day up/down)
- **Logging:** Google Sheets (via Google Sheets API)
- **Alerts:** Telegram bot notifications
- **Frontend:** Streamlit dashboard

---

## 📁 Project Structure

```
Algo_trading/
│
├── app.py                  # Streamlit dashboard (main frontend)
├── backupapp.py            # Alternate Streamlit app
├── test.py                 # Telegram bot test
├── telegrambackup.py       # Telegram alert backup
├── requirements.txt
├── .env                    # Environment variables (DO NOT COMMIT)
│
├── config/
│   ├── config.py           # Loads .env, config constants
│   └── cred.json           # Google Sheets API credentials
│
├── core/
│   ├── backtest.py         # Backtesting logic
│   ├── ml_model.py         # ML model & feature engineering
│   ├── strategy.py         # Signal generation
│   └── utils.py
│
├── data/
│   ├── data_fetcher.py     # Yahoo Finance data fetcher
│   └── dummy_data/
│
├── main/
│   ├── automation.py       # Pipeline runner
│   └── api.py
│
└── services/
    ├── gsheet_logger.py    # Google Sheets logging
    └── telegram_alert.py   # Telegram alert functions
```

---

## ⚙️ Setup & Installation

1. **Clone the repo & install dependencies**
    ```sh
    pip install -r requirements.txt
    ```

2. **Environment Variables**

    Create a `.env` file in the root with:
    ```
    TELEGRAM_BOT_TOKEN=your_telegram_bot_token
    TELEGRAM_CHAT_ID=your_telegram_chat_id
    GOOGLE_SHEETS_CREDENTIALS_PATH=config/cred.json
    GOOGLE_SHEET_NAME=YourGoogleSheetName
    ```

3. **Google Sheets API Setup**
    - Go to [Google Cloud Console](https://console.cloud.google.com/)
    - Create a new project
    - Go to **APIs & Services > Library**
    - Enable **Google Sheets API** and **Google Drive API**
    - Go to **APIs & Services > Credentials**
    - Click **Create Credentials > Service Account**
    - Download the `cred.json` file and place it in the `config/` folder
    - Share your Google Sheet with the service account email (found in `cred.json`)

4. **Telegram Bot Setup**
    - Create a bot via [@BotFather](https://t.me/BotFather) on Telegram
    - Get the bot token and set it in `.env`
    - Get your chat ID (use the `/start` command with your bot and check logs or use a tool like [userinfobot](https://t.me/userinfobot))

---

## 🧠 ML Data Preparation

- **Feature Engineering:**  
  - RSI (Relative Strength Index)
  - MACD & MACD Signal
  - Moving Averages (5, 20)
  - Volume

- **Target Label:**  
  - `Target = 1` if next day's Close > today's Close (i.e., price goes UP)
  - `Target = 0` otherwise

- **ML Algorithm:**  
  - **Logistic Regression** (from `sklearn`)
  - Train/test split (80/20, no shuffle)
  - Outputs: accuracy, classification report, confusion matrix, next-day prediction
  - It can be enhanced by using ensemble technique (XgBoost, Light GBM) or TimeGPT due to time series data. 

---

## 🔗 API & Data Flow

- **Data Fetching:**  
  - Uses Yahoo Finance API via `yfinance`
  - Data stored in-memory as Pandas DataFrames

- **Google Sheets Logging:**  
  - Uses `gspread` and service account credentials
  - Logs trades and summary stats to separate tabs in your Google Sheet

- **Telegram Alerts:**  
  - Uses `python-telegram-bot`
  - Sends pipeline status, trade alerts, and error notifications

---

## 🖥️ Running the Project

1. **Start Telegram Listener (for chat commands & alerts):**
    ```sh
    python services/telegram_alert.py
    ```
    - This must be running to receive `/start` and `/help` commands, and to send alerts.

2. **Start the Streamlit Dashboard:**
    ```sh
    streamlit run app.py
    ```
    - Use the dashboard to select a stock, run the pipeline, and view results.

---

## 📝 Notes

- **All credentials and sensitive info should be kept in `.env` and `config/cred.json` (never commit these!).**
- **Google Sheets logging requires sharing the sheet with your service account email.**
- **Telegram alerts require both bot token and chat ID.**
- **ML model is simple and for demonstration; you can extend with more features or models.**
