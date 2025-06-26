# config/config.py

import os
from dotenv import load_dotenv

# Load .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

# === Feature Toggles ===
USE_DUMMY_DATA = os.getenv("USE_DUMMY_DATA", "False") == "True"
USE_ML_PREDICTIONS = os.getenv("USE_ML_PREDICTIONS", "False") == "True"
LOG_TO_SHEETS = os.getenv("LOG_TO_SHEETS", "True") == "True"
ENABLE_TELEGRAM_ALERTS = os.getenv("ENABLE_TELEGRAM_ALERTS", "False") == "True"

# === Data & API Keys ===
GOOGLE_SHEETS_CREDENTIALS_PATH = os.getenv("GOOGLE_SHEETS_CREDENTIALS_PATH")
GOOGLE_SHEET_NAME = os.getenv("GOOGLE_SHEET_NAME")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# === Strategy Parameters ===
DEFAULT_SYMBOLS = ["RELIANCE.NS", "TCS.NS", "INFY.NS"]
DEFAULT_INTERVAL = "1d"  # or "15m" for intraday
DEFAULT_LOOKBACK = "2y"


# Add fallback plotting with RSI & MA?
# Add logic to force close a trade on last row?
