import os
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout

class ModelTraining:
    def __init__(self, X_train, y_train, output_dir, stock_name):
        self.X_train = X_train
        self.y_train = y_train
        self.output_dir = output_dir
        self.stock_name = stock_name
        self.model = self.build_model()

    def build_model(self):
        model = Sequential()
        model.add(LSTM(units=50, return_sequences=True, input_shape=(self.X_train.shape[1], self.X_train.shape[2])))
        model.add(Dropout(0.2))
        model.add(LSTM(units=50))
        model.add(Dropout(0.2))
        model.add(Dense(1))
        model.compile(optimizer='adam', loss='mean_squared_error')
        return model

    def train_model(self):
        self.model.fit(self.X_train, self.y_train, epochs=25, batch_size=64)
        model_path = os.path.join(self.output_dir, f"{self.stock_name}_lstm_model.h5")
        self.model.save(model_path)
        print(f"LSTM model saved to {model_path}")
        return self.model
