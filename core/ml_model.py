# core/ml_model.py

import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split


# === Feature Engineering ===
def add_technical_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # RSI
    delta = df["Close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(14, min_periods=1).mean()
    avg_loss = loss.rolling(14, min_periods=1).mean()
    rs = avg_gain / avg_loss
    df["RSI"] = 100 - (100 / (1 + rs))

    # Moving Averages
    df["MA_5"] = df["Close"].rolling(window=5).mean()
    df["MA_20"] = df["Close"].rolling(window=20).mean()

    # MACD
    ema_12 = df["Close"].ewm(span=12, adjust=False).mean()
    ema_26 = df["Close"].ewm(span=26, adjust=False).mean()
    df["MACD"] = ema_12 - ema_26
    df["MACD_Signal"] = df["MACD"].ewm(span=9, adjust=False).mean()

    return df


# === Label Generation ===
def generate_labels(df: pd.DataFrame) -> pd.DataFrame:
    """
    Label = 1 if next day's Close is higher, else 0.
    """
    df["Target"] = (df["Close"].shift(-1) > df["Close"]).astype(int)
    return df


# === ML Training ===
def train_predict_model(df: pd.DataFrame):
    df = add_technical_indicators(df)
    df = generate_labels(df)
    df.dropna(inplace=True)

    features = ["RSI", "MACD", "MACD_Signal", "MA_5", "MA_20", "Volume"]
    X = df[features]
    y = df["Target"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, shuffle=False, test_size=0.2
    )

    model = LogisticRegression(max_iter=500)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, output_dict=True)
    report_df = pd.DataFrame(report).transpose()
    cm = confusion_matrix(y_test, y_pred)

    next_day_features = X.iloc[[-1]]
    next_day_prediction = model.predict(next_day_features)[0]

    return {
        "model": model,
        "accuracy": round(accuracy * 100, 2),
        "next_day_prediction": "UP" if next_day_prediction == 1 else "DOWN",
        "training_df": df[features + ["Target"]],
        "classification_report_df": report_df,
        "confusion_matrix": cm,
        "y_true": y_test,
        "y_pred": y_pred,
    }
