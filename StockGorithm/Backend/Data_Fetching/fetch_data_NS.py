import json
import yfinance as yf
import pytz
import pandas as pd
def get_data(stock_name):
    ticker = yf.Ticker(stock_name)
    data = ticker.history(period="1d", interval="5m")

    # Convert time to Indian time zone
    data.index = data.index.tz_convert(pytz.timezone("Asia/Kolkata"))

    # If it's a multi-level column (e.g., TCS.NS under Open/Close), flatten it
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    # Build simplified list of dicts with selected fields
    lister = []

    for index, row in data.iterrows():
        temp = {
            'Time': index.strftime('%Y-%m-%d %H:%M:%S'),
            'Open': round(row['Open'], 2),
            'Close': round(row['Close'], 2),
            'High': round(row['High'], 2),
            'Low': round(row['Low'], 2)
        }
        lister.append(temp)
    return lister

def dummpy_data(cursor):

    # Fetch all stock data
    cursor.execute("SELECT * FROM stock_data ORDER BY Time")
    rows = cursor.fetchall()

    # Format data into dictionary
    stock_dict = {
        "stock_data": [
            {
                "Time": row["time"].strftime("%Y-%m-%d %H:%M:%S"),
                "Open": float(row["open"]),
                "High": float(row["high"]),
                "Low": float(row["low"]),
                "Close": float(row["close"])
            }
            for row in rows
        ]
    }
    # cursor.close()
    # Optional: Print the result as JSON string
    return stock_dict

    # Cleanup
    