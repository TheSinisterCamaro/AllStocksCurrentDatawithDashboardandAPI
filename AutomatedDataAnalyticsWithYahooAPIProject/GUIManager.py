import tkinter as tk
from tkinter import ttk
import threading
import time
import os
from ThreadManager import ThreadManager
from AnalysisManager import AnalysisManager

class GUIManager:
    def __init__(self, analysis_manager, stop_flag):
        self.analysis_manager = analysis_manager
        self.stop_flag = stop_flag
        self.root = None

    def on_run_analysis(self, stock_ticker, progress_var, detail_var, running_var):
        self.stop_flag.clear()
        running_var.set("Running...")
        threading.Thread(target=self.update_running_label, args=(running_var,)).start()
        analysis_thread = threading.Thread(target=self.analysis_manager.run_full_analysis_gui, args=(stock_ticker, progress_var, detail_var))
        analysis_thread.start()

    def on_end_program(self):
        self.stop_flag.set()
        if self.root is not None:
            self.root.destroy()  # Safely close the GUI
        os._exit(0)

    def update_running_label(self, running_var):
        while running_var.get() != "" and not self.stop_flag.is_set():
            current_text = running_var.get()
            if current_text == "Running...":
                running_var.set("Running")
            else:
                running_var.set(current_text + ".")
            if self.root is not None:
                self.root.update_idletasks()
            time.sleep(0.5)

    def setup_gui(self):
        self.root = tk.Tk()  # Create the main window
        self.root.title("Stock Analysis Tool")

        # Pass self.root to the AnalysisManager
        self.analysis_manager.root = self.root

        tk.Label(self.root, text="Enter Stock Ticker:").grid(row=0, column=0, padx=10, pady=10)
        ticker_entry = tk.Entry(self.root)
        ticker_entry.grid(row=0, column=1, padx=10, pady=10)

        progress_var = tk.DoubleVar()
        progress_bar = ttk.Progressbar(self.root, variable=progress_var, maximum=100)
        progress_bar.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        detail_var = tk.StringVar()
        detail_label = tk.Label(self.root, textvariable=detail_var, wraplength=400)
        detail_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        running_var = tk.StringVar()
        running_label = tk.Label(self.root, textvariable=running_var)
        running_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        run_button = tk.Button(self.root, text="Run Analysis", command=lambda: self.on_run_analysis(ticker_entry.get().strip().upper(), progress_var, detail_var, running_var))
        run_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        end_button = tk.Button(self.root, text="End", command=self.on_end_program)
        end_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        self.root.mainloop()  # Start the Tkinter event loop

if __name__ == "__main__":
    # Assuming AnalysisManager and ThreadManager classes are defined elsewhere and imported properly
    thread_manager = ThreadManager()
    stop_flag = thread_manager.get_stop_flag()

    # Initialize other managers (assuming they're imported and implemented)
    analysis_manager = AnalysisManager(data_manager=None, model_manager=None, plot_manager=None, dashboard_manager=None, stop_flag=stop_flag)

    gui_manager = GUIManager(analysis_manager, stop_flag)
    gui_manager.setup_gui()
