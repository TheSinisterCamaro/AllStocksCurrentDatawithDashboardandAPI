import pandas as pd
import numpy as np
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler

class DataProcessing:
    def __init__(self, ticker, start_date):
        self.ticker = ticker
        self.start_date = start_date

    def collect_and_clean_data(self):
        end_date = pd.Timestamp.now()
        data = yf.download(self.ticker, start=self.start_date, end=end_date, interval='1d')
        data.interpolate(method='linear', inplace=True)
        return data

    def prepare_lstm_data_with_features(self, data, look_back=90):
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
