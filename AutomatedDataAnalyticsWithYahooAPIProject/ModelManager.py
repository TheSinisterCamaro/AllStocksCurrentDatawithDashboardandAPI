from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout
import os
import numpy as np
import pandas as pd
import datetime as dt

class ModelManager:
    def __init__(self, stop_flag):
        self.stop_flag = stop_flag

    def check_stop(self):
        if self.stop_flag.is_set():
            raise SystemExit("Analysis stopped by the user.")

    def train_lstm_model(self, X_train, y_train, output_dir, stock_name):
        self.check_stop()
        model = Sequential()
        model.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2])))
        model.add(Dropout(0.2))
        model.add(LSTM(units=50))
        model.add(Dropout(0.2))
        model.add(Dense(1))
        model.compile(optimizer='adam', loss='mean_squared_error')
        model.fit(X_train, y_train, epochs=25, batch_size=64)
        model_path = os.path.join(output_dir, f"{stock_name}_lstm_model.h5")
        model.save(model_path)
        print(f"LSTM model saved to {model_path}")
        return model

    def predict_future_prices_lstm(self, model, data, scaler, output_dir, stock_name, look_back=90, future_days=365):
        self.check_stop()
        last_data = data[-look_back:].values
        scaled_last_data = scaler.transform(last_data)
        future_inputs = np.reshape(scaled_last_data, (1, look_back, scaled_last_data.shape[1]))
        predictions = []
        for _ in range(future_days):
            self.check_stop()
            pred = model.predict(future_inputs)
            predictions.append(pred[0, 0])
            future_inputs = np.roll(future_inputs, -1, axis=1)
            future_inputs[0, -1, 0] = pred
        closing_price_predictions = np.array(predictions).reshape(-1, 1)
        dummy_scaled_data = np.zeros((closing_price_predictions.shape[0], scaler.n_features_in_))
        dummy_scaled_data[:, 0] = closing_price_predictions.flatten()
        inverse_transformed_predictions = scaler.inverse_transform(dummy_scaled_data)[:, 0]
        future_dates = [data.index[-1] + dt.timedelta(days=i) for i in range(1, future_days + 1)]
        forecast_series = pd.Series(inverse_transformed_predictions.flatten(), index=future_dates)
        forecast_series.to_csv(os.path.join(output_dir, f"{stock_name}_lstm_future_predictions.csv"))
        print(f"Future predictions saved to {output_dir}")
        return forecast_series
