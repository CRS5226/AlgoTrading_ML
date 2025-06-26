# services/gsheet_logger.py

import gspread
import pandas as pd
from config.config import GOOGLE_SHEETS_CREDENTIALS_PATH, GOOGLE_SHEET_NAME


def get_gsheet_client():
    """Authorize and return Google Sheets client."""
    gc = gspread.service_account(filename=GOOGLE_SHEETS_CREDENTIALS_PATH)
    sh = gc.open(GOOGLE_SHEET_NAME)
    return sh


def log_trades(trades_df: pd.DataFrame, sheet_name="Trades"):
    """Log individual trades to a sheet tab."""
    if trades_df.empty:
        print("[INFO] No trades to log.")
        return

    sh = get_gsheet_client()

    try:
        worksheet = sh.worksheet(sheet_name)
        worksheet.clear()
    except gspread.exceptions.WorksheetNotFound:
        worksheet = sh.add_worksheet(title=sheet_name, rows="100", cols="20")

    # Convert all datetime columns to strings before upload
    df_to_upload = trades_df.copy()
    for col in df_to_upload.select_dtypes(include=['datetime64[ns]']).columns:
        df_to_upload[col] = df_to_upload[col].dt.strftime('%Y-%m-%d %H:%M:%S')  # Format as string

    # Convert any remaining non-serializable types to strings
    for col in df_to_upload.columns:
        if df_to_upload[col].dtype == 'object':
            continue
        try:
            df_to_upload[col] = df_to_upload[col].astype(str)
        except Exception as e:
            print(f"[WARNING] Could not convert column '{col}' to string: {e}")

    # Update the worksheet with the DataFrame
    worksheet.update([df_to_upload.columns.values.tolist()] + df_to_upload.values.tolist())

    print(f"[INFO] Trades logged to Google Sheet: {sheet_name}")




def log_summary(stats: dict, sheet_name="Summary"):
    """Log stats summary to another tab."""
    sh = get_gsheet_client()

    try:
        worksheet = sh.worksheet(sheet_name)
        worksheet.clear()
    except gspread.exceptions.WorksheetNotFound:
        worksheet = sh.add_worksheet(title=sheet_name, rows="20", cols="2")

    # Convert dict to DataFrame for clean update
    df_stats = pd.DataFrame(stats.items(), columns=["Metric", "Value"])
    worksheet.update([df_stats.columns.values.tolist()] + df_stats.values.tolist())
    print(f"[INFO] Summary stats logged to Google Sheet: {sheet_name}")
