import matplotlib.pyplot as plt

class Plotting:
    def __init__(self, data, output_dir, stock_name):
        self.data = data
        self.output_dir = output_dir
        self.stock_name = stock_name

    def plot_and_save_graphs(self):
        plt.figure(figsize=(10, 6))
        plt.plot(self.data['Close'], label='Close Price')
        plt.plot(self.data['MA_20'], label='20-Day Moving Average')
        plt.plot(self.data['MA_50'], label='50-Day Moving Average')
        plt.title(f'{self.stock_name} Historical Prices with Moving Averages')
        plt.xlabel('Date')
        plt.ylabel('Price (USD)')
        plt.legend()
        plt.savefig(os.path.join(self.output_dir, f"{self.stock_name}_historical_prices_moving_averages.png"))
        plt.close()

        plt.figure(figsize=(10, 6))
        plt.plot(self.data['RSI'], label='RSI')
        plt.axhline(30, linestyle='--', color='red')
        plt.axhline(70, linestyle='--', color='red')
        plt.title(f'{self.stock_name} Relative Strength Index (RSI)')
        plt.xlabel('Date')
        plt.ylabel('RSI')
        plt.legend()
        plt.savefig(os.path.join(self.output_dir, f"{self.stock_name}_RSI.png"))
        plt.close()

        plt.figure(figsize=(10, 6))
        plt.plot(self.data['Volatility'], label='Volatility')
        plt.title(f'{self.stock_name} Volatility')
        plt.xlabel('Date')
        plt.ylabel('Volatility')
        plt.legend()
        plt.savefig(os.path.join(self.output_dir, f"{self.stock_name}_Volatility.png"))
        plt.close()
