import os
import tensorflow as tf
import logging
import warnings
import yfinance as yf
import pandas as pd
import numpy as np
import datetime as dt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout
import matplotlib.pyplot as plt
import dash
from dash import dcc, html
import plotly.graph_objs as go
import threading
import tkinter as tk
from tkinter import ttk
import time
from ConfigManager import ConfigManager
from DataManager import DataManager
from ModelManager import ModelManager
from PlotManager import PlotManager
from DashboardManager import DashboardManager
from AnalysisManager import AnalysisManager
from GUIManager import GUIManager
from ThreadManager import ThreadManager

# Initialize ConfigManager to set up the environment
config_manager = ConfigManager()

if __name__ == "__main__":
    # Initialize ThreadManager and stop flag
    thread_manager = ThreadManager()
    stop_flag = thread_manager.get_stop_flag()

    # Initialize all managers properly
    data_manager = DataManager(stop_flag)
    model_manager = ModelManager(stop_flag)
    plot_manager = PlotManager(stop_flag)
    dashboard_manager = DashboardManager()

    # Pass the initialized managers to AnalysisManager
    analysis_manager = AnalysisManager(
        data_manager=data_manager,
        model_manager=model_manager,
        plot_manager=plot_manager,
        dashboard_manager=dashboard_manager,
        stop_flag=stop_flag,
        root=None  # Remove root=None if it's not used here
    )

    # Initialize GUIManager with the AnalysisManager and stop flag
    gui_manager = GUIManager(analysis_manager, stop_flag)

    # Set up and run the GUI
    gui_manager.setup_gui()
