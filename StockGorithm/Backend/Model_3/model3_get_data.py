import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler
import pickle
from tensorflow.keras.models import load_model


# Function to fetch stock data
def model3_get_data(scaler_x,scaler_y):
    def fetch_stock_data(ticker):
        stock = yf.Ticker(ticker)

        # Fetching intraday data (5min intervals) with the maximum allowed period (60 days)
        data = stock.history(period="3d", interval="5m")
        return data

    # Example usage
    ticker_symbol = "INFY.NS"  # Apple Inc.
    stock_data = fetch_stock_data(ticker_symbol)
    # Display fetched data
    print(stock_data)



    # Assuming 'stock_data' is your DataFrame that contains the columns 'Open', 'High', 'Low', 'Close', 'Volume'

    # 1. Calculate RSI (Relative Strength Index)
    def calculate_rsi(data, window=14):
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()

        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))

        return rsi

    # 2. Calculate Pivot Points and Support/Resistance Levels
    def calculate_pivot_points(data):
        data['Pivot'] = (data['High'] + data['Low'] + data['Close']) / 3
        data['R1'] = 2 * data['Pivot'] - data['Low']
        data['S1'] = 2 * data['Pivot'] - data['High']
        data['R2'] = data['Pivot'] + (data['High'] - data['Low'])
        data['S2'] = data['Pivot'] - (data['High'] - data['Low'])

        return data

    # 3. Calculate MACD (Moving Average Convergence Divergence)
    def calculate_macd(data, fast_period=12, slow_period=26, signal_period=9):
        # Calculate MACD
        data['EMA_12'] = data['Close'].ewm(span=fast_period, adjust=False).mean()
        data['EMA_26'] = data['Close'].ewm(span=slow_period, adjust=False).mean()
        data['MACD'] = data['EMA_12'] - data['EMA_26']

        # Calculate Signal Line
        data['MACD_Signal'] = data['MACD'].ewm(span=signal_period, adjust=False).mean()

        return data

    # Assuming 'stock_data' is the DataFrame containing the stock data with 'Open', 'Close', 'High', 'Low', 'Volume'
    # Example usage:

    # Calculate the indicators
    stock_data['RSI'] = calculate_rsi(stock_data)
    stock_data = calculate_pivot_points(stock_data)
    stock_data = calculate_macd(stock_data)

    # Print the resulting DataFrame
    print(stock_data)


    data = stock_data.copy()
    data.reset_index(inplace=True)

    data.drop(columns=['Dividends','Stock Splits','Datetime'],inplace=True)

    data.dropna(inplace=True)

    data_np = data.to_numpy()



    # Assuming data_np is your numpy array, and we're scaling RSI and MACD for 'x' and the 'Close' for 'y'

    x = []
    y = []

    # Ensure data_np is large enough
    if len(data_np) < 100:
        raise ValueError("data_np must have at least 100 rows")

    # Collecting data for x and y
    for i in range(100, len(data_np)):
        # Collecting features over the past 100 periods
        close_temp = data_np[i-100:i, 3]   # Close value (3rd column) over the past 100 periods
        volume_temp = data_np[i-100:i, 4]
        rsi_temp3 = data_np[i-100:i, 5]  # RSI values (5th column)
        macd_temp = data_np[i-100:i, 6]  # MACD values (6th column)
        # Volume (4th column) over the past 100 periods
        seven_temp = data_np[i-100:i, 7] # Example feature (7th column) over the past 100 periods
        eight_temp = data_np[i-100:i, 8] # Example feature (8th column) over the past 100 periods
        nine_temp = data_np[i-100:i, 9]  # Example feature (9th column) over the past 100 periods
        ten_temp = data_np[i-100:i, 10]  # Example feature (10th column) over the past 100 periods
        ten_temp1 = data_np[i-100:i, 11]
        ten_temp2 = data_np[i-100:i, 12]
        ten_temp3 = data_np[i-100:i, 13]
        ten_temp4 = data_np[i-100:i, 14]

        # Stack these features together along the second axis (axis=1)
        sample = np.stack([close_temp,volume_temp,rsi_temp3,macd_temp,seven_temp,eight_temp,nine_temp,ten_temp,ten_temp1,ten_temp2,ten_temp3,ten_temp4], axis=0)

        # Append the stacked features as a single sample to x
        x.append(sample)

        # Target variable y is the current close price (at index i)
        y.append(data_np[i, 3])  # Close price (3rd column)

    # Convert x and y to numpy arrays
    x = np.array(x)  # Shape will be (num_samples, 8, 100)
    y = np.array(y)  # Shape will be (num_samples,)

    # Now, let's reshape x to have the shape (num_samples, 6, 100) by selecting only the first 6 features
    x = x[:, :, :]  # Select only the first 6 features (i.e., RSI, MACD, Close, Volume, Seven, Eight)

    # Final shapes of x and y
    print(f"x shape: {x.shape}")
    print(f"y shape: {y.shape}")


    


    x_reshaped = x.reshape(-1, x.shape[-1])  # Flattening (num_samples, 6, 100) to (num_samples, 600)


    # Scale x
    x_scaled = scaler_x.transform(x_reshaped)  # Scale x to [0, 1]

    # Reshape x back to (num_samples, 6, 100) after scaling
    x_scaled = x_scaled.reshape(x.shape)  # Reshape back to the original shape (num_samples, 6, 100)

    y_scaled = scaler_y.transform(y.reshape(-1, 1))  # Scale y to [0, 1]

    # Final shapes of scaled x and y
    print(f"Scaled x shape: {x_scaled.shape}")
    print(f"Scaled y shape: {y_scaled.shape}")


    test_one = np.expand_dims(x_scaled[-1], axis=0)
    print(test_one)
    return test_one,float(stock_data.Close.iloc[-1]),stock_data.index[-1]





def model3_load_model():
    model = load_model(r'Model_3/lstm_model_INFY.keras')
    with open(r'Model_3\scaler_x_INFY.pkl', 'rb') as f:
        scaler_x = pickle.load(f)
    with open(r'Model_3\scaler_y_INFY.pkl', 'rb') as f:
        scaler_y = pickle.load(f)
    return model,scaler_x,scaler_y


def model3_predict(model,test_data,scaler_y):
    prediction_result = model.predict(test_data)
    prediction_result = scaler_y.inverse_transform(prediction_result)
    return prediction_result[0][0]



