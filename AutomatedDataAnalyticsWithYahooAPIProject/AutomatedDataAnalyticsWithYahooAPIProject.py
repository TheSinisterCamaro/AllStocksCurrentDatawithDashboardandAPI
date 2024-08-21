import tkinter as tk
from tkinter import ttk, messagebox
from multiprocessing import Process, Value, Manager
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import datetime as dt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout
from datetime import timedelta
from dash import dcc, html
import dash
import plotly.graph_objs as go

# Function to update progress in the GUI
def update_progress(progress_var, detail_var, progress_value, detail_text):
    progress_var.set(progress_value)
    detail_var.set(detail_text)

# Function to run the full analysis and update progress
def run_full_analysis_gui(ticker, progress, detail_text):
    date_time_suffix = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    base_output_dir = r"C:\Users\jdick\source\repos\AutomatedDataAnalyticsWithYahooAPIProject"
    output_dir = create_directory(base_output_dir, ticker, date_time_suffix)

    # Update progress
    progress.value = 10
    detail_text.value = "Collecting and cleaning data..."
    ubs_data = collect_and_clean_data(ticker, "2010-01-01", interval='1d')

    # Prepare data for LSTM
    progress.value = 30
    detail_text.value = "Preparing data for LSTM..."
    X_train, y_train, scaler = prepare_lstm_data_with_features(ubs_data)

    # Train model
    progress.value = 50
    detail_text.value = "Training LSTM model..."
    lstm_model = train_lstm_model(X_train, y_train, output_dir, ticker)

    # Plot and save graphs
    progress.value = 70
    detail_text.value = "Plotting and saving graphs..."
    plot_and_save_graphs(ubs_data, output_dir, ticker)

    # Predict future prices
    progress.value = 90
    detail_text.value = "Predicting future prices..."
    future_predictions = predict_future_prices_lstm(lstm_model, ubs_data, scaler, output_dir, ticker, future_days=365)

    # Finalize
    progress.value = 100
    detail_text.value = f"Analysis complete! View results at: {output_dir}\nVisit the dashboard at http://127.0.0.1:8050/"
    start_dashboard(ubs_data, future_predictions, ticker)

# Function to handle running analysis from the GUI
def run_analysis_gui(stock_ticker, progress_var, detail_var):
    manager = Manager()
    progress = Value('d', 0.0)
    detail_text = manager.Value(str, "")

    def update_progress_in_gui():
        while progress.value < 100:
            update_progress(progress_var, detail_var, progress.value, detail_text.value)
            root.update_idletasks()
        update_progress(progress_var, detail_var, 100, detail_text.value)  # Ensure the progress bar fills up

    p = Process(target=run_full_analysis_gui, args=(stock_ticker, progress, detail_text))
    p.start()

    update_progress_in_gui()

# Function to create a directory with a date-time suffix
def create_directory(base_path, stock_name, suffix):
    directory_path = os.path.join(base_path, f"{stock_name}_results_{suffix}")
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    return directory_path

# Function to collect and clean data
def collect_and_clean_data(ticker, start_date, interval='1d'):
    end_date = dt.datetime.now()
    data = yf.download(ticker, start=start_date, end=end_date, interval=interval)
    if data.isnull().values.any():
        print("Missing values detected. Applying linear interpolation...")
        data.interpolate(method='linear', inplace=True)
    return data

# Function to prepare LSTM data
def prepare_lstm_data_with_features(data, look_back=90):
    data['MA_20'] = data['Close'].rolling(window=20).mean()
    data['MA_50'] = data['Close'].rolling(window=50).mean()
    data['RSI'] = data['Close'].rolling(window=14).apply(
        lambda x: 100 - (100 / (1 + (x.diff().clip(lower=0).sum() / abs(x.diff().clip(upper=0).sum()))))
    )
    data['Volatility'] = data['Close'].rolling(window=20).std()
    data.dropna(inplace=True)
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data)
    X, y = [], []
    for i in range(look_back, len(scaled_data)):
        X.append(scaled_data[i-look_back:i])
        y.append(scaled_data[i, 0])
    X, y = np.array(X), np.array(y)
    return X, y, scaler

# Function to train the LSTM model
def train_lstm_model(X_train, y_train, output_dir, stock_name):
    model = Sequential()
    model.add(LSTM(units=100, return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2])))
    model.add(Dropout(0.2))
    model.add(LSTM(units=100))
    model.add(Dropout(0.2))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(X_train, y_train, epochs=50, batch_size=32)
    model_path = os.path.join(output_dir, f"{stock_name}_lstm_model.h5")
    model.save(model_path)
    print(f"LSTM model saved to {model_path}")
    return model

# Function to plot and save graphs
def plot_and_save_graphs(data, output_dir, stock_name):
    plt.figure(figsize=(10, 6))
    plt.plot(data['Close'], label='Close Price')
    plt.plot(data['MA_20'], label='20-Day Moving Average')
    plt.plot(data['MA_50'], label='50-Day Moving Average')
    plt.title(f'{stock_name} Historical Prices with Moving Averages')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.legend()
    plt.savefig(os.path.join(output_dir, f"{stock_name}_historical_prices_moving_averages.png"))
    plt.close()

    plt.figure(figsize=(10, 6))
    plt.plot(data['RSI'], label='RSI')
    plt.axhline(30, linestyle='--', color='red')
    plt.axhline(70, linestyle='--', color='red')
    plt.title(f'{stock_name} Relative Strength Index (RSI)')
    plt.xlabel('Date')
    plt.ylabel('RSI')
    plt.legend()
    plt.savefig(os.path.join(output_dir, f"{stock_name}_RSI.png"))
    plt.close()

    plt.figure(figsize=(10, 6))
    plt.plot(data['Volatility'], label='Volatility')
    plt.title(f'{stock_name} Volatility')
    plt.xlabel('Date')
    plt.ylabel('Volatility')
    plt.legend()
    plt.savefig(os.path.join(output_dir, f"{stock_name}_Volatility.png"))
    plt.close()

# Function to predict future prices
def predict_future_prices_lstm(model, data, scaler, output_dir, stock_name, look_back=90, future_days=365):
    last_data = data[-look_back:].values
    scaled_last_data = scaler.transform(last_data)
    future_inputs = np.reshape(scaled_last_data, (1, look_back, scaled_last_data.shape[1]))
    predictions = []
    for _ in range(future_days):
        pred = model.predict(future_inputs)
        predictions.append(pred[0, 0])
        future_inputs = np.roll(future_inputs, -1, axis=1)
        future_inputs[0, -1, 0] = pred
    closing_price_predictions = np.array(predictions).reshape(-1, 1)
    dummy_scaled_data = np.zeros((closing_price_predictions.shape[0], scaler.n_features_in_))
    dummy_scaled_data[:, 0] = closing_price_predictions.flatten()
    inverse_transformed_predictions = scaler.inverse_transform(dummy_scaled_data)[:, 0]
    future_dates = [data.index[-1] + timedelta(days=i) for i in range(1, future_days + 1)]
    forecast_series = pd.Series(inverse_transformed_predictions.flatten(), index=future_dates)
    forecast_series.to_csv(os.path.join(output_dir, f"{stock_name}_lstm_future_predictions.csv"))
    print(f"Future predictions saved to {output_dir}")
    return forecast_series

# Function to create a dashboard
def create_dashboard(data, predictions, stock_name):
    app = dash.Dash(__name__)
    app.layout = html.Div(children=[
        html.H1(children=f'{stock_name} Stock Price Prediction Dashboard'),
        dcc.Graph(
            id='historical-prices',
            figure={
                'data': [
                    go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Historical Close Price'),
                    go.Scatter(x=predictions.index, y=predictions, mode='lines', name='Predicted Close Price')
                ],
                'layout': go.Layout(title=f'{stock_name} Historical and Predicted Prices')
            }
        ),
        dcc.Graph(
            id='rsi-plot',
            figure={
                'data': [
                    go.Scatter(x=data.index, y=data['RSI'], mode='lines', name='RSI')
                ],
                'layout': go.Layout(title='RSI (Relative Strength Index)')
            }
        ),
        dcc.Graph(
            id='volatility-plot',
            figure={
                'data': [
                    go.Scatter(x=data.index, y=data['Volatility'], mode='lines', name='Volatility')
                ],
                'layout': go.Layout(title='Volatility')
            }
        ),
    ])
    app.run_server(debug=False, use_reloader=False)

def start_dashboard(data, predictions, stock_name):
    p = Process(target=create_dashboard, args=(data, predictions, stock_name))
    p.start()

# GUI Setup
def setup_gui():
    global root
    root = tk.Tk()
    root.title("Stock Analysis Tool")

    # Stock Ticker Label and Entry
    tk.Label(root, text="Enter Stock Ticker:").grid(row=0, column=0, padx=10, pady=10)
    ticker_entry = tk.Entry(root)
    ticker_entry.grid(row=0, column=1, padx=10, pady=10)

    # Progress Bar
    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100)
    progress_bar.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

    # Detail Text
    detail_var = tk.StringVar()
    detail_label = tk.Label(root, textvariable=detail_var, wraplength=400)
    detail_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    # Run Analysis Button
    def on_run_analysis():
        stock_ticker = ticker_entry.get().strip().upper()
        if stock_ticker:
            run_analysis_gui(stock_ticker, progress_var, detail_var)

    run_button = tk.Button(root, text="Run Analysis", command=on_run_analysis)
    run_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    # Start the GUI event loop
    root.mainloop()

# Start the GUI
if __name__ == "__main__":
    setup_gui()
