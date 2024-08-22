import dash
from dash import dcc, html
import plotly.graph_objs as go
import threading

class DashboardManager:
    def __init__(self):
        pass

    def create_dashboard(self, data, predictions, stock_name):
        app = dash.Dash(__name__)
        app.layout = html.Div(children=[
            html.H1(children=f'{stock_name} Stock Price Prediction Dashboard'),
            dcc.Graph(
                id='historical-prices',
                figure={
                    'data': [
                        go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Historical Close Price'),
                        go.Scatter(x=predictions.index, y=predictions, mode='lines', name='Predicted Close Price')
                    ],
                    'layout': go.Layout(title=f'{stock_name} Historical and Predicted Prices')
                }
            ),
            dcc.Graph(
                id='rsi-plot',
                figure={
                    'data': [
                        go.Scatter(x=data.index, y=data['RSI'], mode='lines', name='RSI')
                    ],
                    'layout': go.Layout(title='RSI (Relative Strength Index)')
                }
            ),
            dcc.Graph(
                id='volatility-plot',
                figure={
                    'data': [
                        go.Scatter(x=data.index, y=data['Volatility'], mode='lines', name='Volatility')
                    ],
                    'layout': go.Layout(title='Volatility')
                }
            ),
        ])
        app.run_server(debug=False, use_reloader=False)

    def start_dashboard(self, data, predictions, stock_name):
        threading.Thread(target=self.create_dashboard, args=(data, predictions, stock_name)).start()
