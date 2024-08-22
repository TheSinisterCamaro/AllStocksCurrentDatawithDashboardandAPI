from data_processing import DataProcessing
from model_training import ModelTraining
from plotting import Plotting
from dashboard import Dashboard
from gui import StockAnalysisGUI

def main():
    gui = StockAnalysisGUI()
    gui.setup_gui()

if __name__ == "__main__":
    main()
