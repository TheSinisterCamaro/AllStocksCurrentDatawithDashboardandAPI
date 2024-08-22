import tkinter as tk
from tkinter import ttk

class StockAnalysisGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Stock Analysis Tool")
        self.setup_gui()

    def setup_gui(self):
        # Stock Ticker Label and Entry
        tk.Label(self.root, text="Enter Stock Ticker:").grid(row=0, column=0, padx=10, pady=10)
        self.ticker_entry = tk.Entry(self.root)
        self.ticker_entry.grid(row=0, column=1, padx=10, pady=10)

        # Progress Bar
        self.progress_var = tk.DoubleVar()
        progress_bar = ttk.Progressbar(self.root, variable=self.progress_var, maximum=100)
        progress_bar.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        # Detail Text
        self.detail_var = tk.StringVar()
        detail_label = tk.Label(self.root, textvariable=self.detail_var, wraplength=400)
        detail_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        # Running Indicator
        self.running_var = tk.StringVar()
        running_label = tk.Label(self.root, textvariable=self.running_var)
        running_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        # Run Analysis Button
        run_button = tk.Button(self.root, text="Run Analysis", command=self.on_button_click)
        run_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        # End Button
        end_button = tk.Button(self.root, text="End", command=self.on_end_program)
        end_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        # Start the GUI event loop
        self.root.mainloop()

    def on_button_click(self):
        stock_ticker = self.ticker_entry.get().strip().upper()
        if stock_ticker:
            # Place your integration code here
            pass

    def on_end_program(self):
        self.root.destroy()
