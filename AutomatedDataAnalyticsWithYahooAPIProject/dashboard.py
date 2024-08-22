from dash import dcc, html
import dash
import plotly.graph_objs as go
import threading

class Dashboard:
    def __init__(self, data, predictions, stock_name):
        self.data = data
        self.predictions = predictions
        self.stock_name = stock_name

    def create_dashboard(self):
        app = dash.Dash(__name__)
        app.layout = html.Div(children=[
            html.H1(children=f'{self.stock_name} Stock Price Prediction Dashboard'),
            dcc.Graph(
                id='historical-prices',
                figure={
                    'data': [
                        go.Scatter(x=self.data.index, y=self.data['Close'], mode='lines', name='Historical Close Price'),
                        go.Scatter(x=self.predictions.index, y=self.predictions, mode='lines', name='Predicted Close Price')
                    ],
                    'layout': go.Layout(title=f'{self.stock_name} Historical and Predicted Prices')
                }
            ),
            dcc.Graph(
                id='rsi-plot',
                figure={
                    'data': [
                        go.Scatter(x=self.data.index, y=self.data['RSI'], mode='lines', name='RSI')
                    ],
                    'layout': go.Layout(title='RSI (Relative Strength Index)')
                }
            ),
            dcc.Graph(
                id='volatility-plot',
                figure={
                    'data': [
                        go.Scatter(x=self.data.index, y=self.data['Volatility'], mode='lines', name='Volatility')
                    ],
                    'layout': go.Layout(title='Volatility')
                }
            ),
        ])
        app.run_server(debug=False, use_reloader=False)

    def start_dashboard(self):
        threading.Thread(target=self.create_dashboard).start()
