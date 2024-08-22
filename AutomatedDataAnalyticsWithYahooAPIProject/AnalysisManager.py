import datetime as dt
import os
import pandas as pd

class AnalysisManager:
    def __init__(self, data_manager, model_manager, plot_manager, dashboard_manager, stop_flag, root):
        self.data_manager = data_manager
        self.model_manager = model_manager
        self.plot_manager = plot_manager
        self.dashboard_manager = dashboard_manager
        self.stop_flag = stop_flag
        self.root = root  # Pass root as an argument

    def update_progress(self, progress_var, detail_var, progress_value, detail_text):
        if not self.stop_flag.is_set():
            progress_var.set(progress_value)
            detail_var.set(detail_text)
            self.root.update_idletasks()  # Use self.root instead of root

    def run_full_analysis_gui(self, ticker, progress_var, detail_var):
        try:
            date_time_suffix = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
            base_output_dir = r"C:\File\Path\Here"  # Add file path to store results
            output_dir = self.create_directory(base_output_dir, ticker, date_time_suffix)

            self.update_progress(progress_var, detail_var, 10, "Collecting and cleaning data...")
            ubs_data = self.data_manager.collect_and_clean_data(ticker, "2010-01-01", interval='1d')

            self.update_progress(progress_var, detail_var, 30, "Preparing data for LSTM...")
            X_train, y_train, scaler = self.data_manager.prepare_lstm_data_with_features(ubs_data)

            self.update_progress(progress_var, detail_var, 50, "Training LSTM model...")
            lstm_model = self.model_manager.train_lstm_model(X_train, y_train, output_dir, ticker)

            self.update_progress(progress_var, detail_var, 70, "Plotting and saving graphs...")
            self.plot_manager.plot_and_save_graphs(ubs_data, output_dir, ticker)

            self.update_progress(progress_var, detail_var, 90, "Predicting future prices...")
            future_predictions = self.model_manager.predict_future_prices_lstm(lstm_model, ubs_data, scaler, output_dir, ticker, future_days=365)

            self.update_progress(progress_var, detail_var, 100, f"Analysis complete! View results at: {output_dir}\nVisit the dashboard at http://127.0.0.1:8050/")
            self.dashboard_manager.start_dashboard(ubs_data, future_predictions, ticker)
        except SystemExit as e:
            print(f"Analysis stopped: {e}")
            os._exit(0)
        except Exception as e:
            print(f"An error occurred: {e}")
            os._exit(1)

    def create_directory(self, base_path, stock_name, suffix):
        directory_path = os.path.join(base_path, f"{stock_name}_results_{suffix}")
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
        return directory_path
