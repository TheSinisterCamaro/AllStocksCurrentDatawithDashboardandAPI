import matplotlib.pyplot as plt
import os

class PlotManager:
    def __init__(self, stop_flag):
        self.stop_flag = stop_flag

    def check_stop(self):
        if self.stop_flag.is_set():
            raise SystemExit("Analysis stopped by the user.")

    def plot_and_save_graphs(self, data, output_dir, stock_name):
        self.check_stop()
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
