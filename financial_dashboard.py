import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import datetime
import time
import os
from flask_cors import CORS

# Import configuration
try:
    from config import *
except ImportError:
    # Fallback configuration if config.py is not available
    SERVER_HOST = '0.0.0.0'
    SERVER_PORT = 12001
    DEBUG_MODE = True
    DASHBOARD_TITLE = "Financial Assets Dashboard"
    UPDATE_INTERVAL_SECONDS = 20
    CURRENT_PRICES = {
        'Gold': 3200, 'Silver': 37, 'TSLA': 280,
        'Bitcoin': 105000, 'Ethereum': 5800, 'XRP': 1.25
    }
    CHART_COLORS = {
        'Gold': '#FFD700', 'Silver': '#C0C0C0', 'Gold_Silver_Ratio': '#B87333',
        'TSLA': '#E31937', 'Bitcoin': '#F7931A', 'Ethereum': '#627EEA',
        'BTC_ETH_Ratio': '#8A2BE2', 'XRP': '#23292F'
    }
    VOLATILITY_PARAMS = {
        'Gold': {'volatility': 0.008, 'mean_reversion': 0.02},
        'Silver': {'volatility': 0.015, 'mean_reversion': 0.03},
        'TSLA': {'volatility': 0.025, 'mean_reversion': 0.01},
        'Bitcoin': {'volatility': 0.03, 'mean_reversion': 0.015},
        'Ethereum': {'volatility': 0.035, 'mean_reversion': 0.02},
        'XRP': {'volatility': 0.025, 'mean_reversion': 0.02}
    }
    HISTORICAL_DAYS = 30
    DATA_FREQUENCY = 'h'

# Create assets directory if it doesn't exist
os.makedirs('assets', exist_ok=True)

# Create a Dash app
app = dash.Dash(__name__, 
                suppress_callback_exceptions=True,
                meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}])
server = app.server
CORS(server)  # Enable CORS for all routes

# Set the title of the dashboard
app.title = DASHBOARD_TITLE

# Function to generate mock data for assets
def generate_mock_data(asset_name, days=None, freq=None):
    """Generate realistic mock data for financial assets with mean reversion"""
    if days is None:
        days = HISTORICAL_DAYS
    if freq is None:
        freq = DATA_FREQUENCY
        
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=days)
    
    # Create date range
    dates = pd.date_range(start=start_date, end=end_date, freq=freq)
    n = len(dates)
    
    # Set parameters based on asset
    if asset_name in CURRENT_PRICES and asset_name in VOLATILITY_PARAMS:
        current_price = CURRENT_PRICES[asset_name]
        volatility = VOLATILITY_PARAMS[asset_name]['volatility']
        mean_reversion = VOLATILITY_PARAMS[asset_name]['mean_reversion']
    else:
        current_price = 100
        volatility = 0.01
        mean_reversion = 0.01
    
    # Generate price series with mean reversion
    prices = [current_price * 0.9 + current_price * 0.1 * np.random.normal()]  # Start near current price
    
    for i in range(1, n):
        # Mean reversion component
        mean_reversion_component = mean_reversion * (current_price - prices[-1])
        # Random component
        random_component = volatility * prices[-1] * np.random.normal()
        # New price
        new_price = prices[-1] * (1 + mean_reversion_component + random_component)
        # Ensure price doesn't go negative
        new_price = max(new_price, 0.001 * current_price)
        prices.append(new_price)
    
    # Ensure the last price is close to the current market price
    prices[-1] = current_price * (0.995 + 0.01 * np.random.random())
    
    # Create DataFrame
    df = pd.DataFrame({
        'Date': dates,
        'Price': prices
    })
    
    return df

# Function to create ratio data
def create_ratio_data(df1, df2, name1, name2):
    """Create ratio data from two dataframes"""
    # Ensure both dataframes have the same dates
    merged = pd.merge(df1, df2, on='Date', suffixes=('_1', '_2'))
    merged['Ratio'] = merged['Price_1'] / merged['Price_2']
    merged = merged[['Date', 'Ratio']]
    merged.columns = ['Date', 'Price']  # Rename for consistency
    return merged

# Function to create a chart
def create_chart(df, title, color='#1f77b4'):
    """Create a plotly chart from dataframe"""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['Date'],
        y=df['Price'],
        mode='lines',
        name=title,
        line=dict(color=color, width=2),
        hovertemplate='%{y:.2f}<extra></extra>'
    ))
    
    # Add current price annotation
    current_price = df['Price'].iloc[-1]
    fig.add_annotation(
        x=df['Date'].iloc[-1],
        y=current_price,
        text=f"${current_price:.2f}" if current_price > 1 else f"${current_price:.4f}",
        showarrow=True,
        arrowhead=1,
        ax=50,
        ay=-40
    )
    
    # Set layout
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=16),
            x=0.5,
            xanchor='center'
        ),
        margin=dict(l=40, r=40, t=40, b=40),
        hovermode='x unified',
        plot_bgcolor='rgba(250,250,250,0.9)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(230,230,230,0.8)',
            showline=True,
            linecolor='rgba(0,0,0,0.2)',
            linewidth=1
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(230,230,230,0.8)',
            showline=True,
            linecolor='rgba(0,0,0,0.2)',
            linewidth=1,
            tickprefix='$' if 'Ratio' not in title else ''
        )
    )
    
    return fig

# Define the layout of the dashboard
app.layout = html.Div([
    # Header
    html.Div([
        html.H1(DASHBOARD_TITLE, className="dashboard-title"),
        html.Div([
            html.Span("Last Updated: ", className="update-label"),
            html.Span(id="update-time", className="update-time"),
            html.Span(id="update-status", className="update-status")
        ], className="update-info")
    ], className="header"),
    
    # Main content
    html.Div([
        # First row of charts
        html.Div([
            html.Div([
                dcc.Graph(id='gold-chart', className="chart")
            ], className="chart-container"),
            html.Div([
                dcc.Graph(id='silver-chart', className="chart")
            ], className="chart-container"),
            html.Div([
                dcc.Graph(id='gold-silver-ratio-chart', className="chart")
            ], className="chart-container"),
            html.Div([
                dcc.Graph(id='tsla-chart', className="chart")
            ], className="chart-container")
        ], className="chart-row"),
        
        # Second row of charts
        html.Div([
            html.Div([
                dcc.Graph(id='bitcoin-chart', className="chart")
            ], className="chart-container"),
            html.Div([
                dcc.Graph(id='ethereum-chart', className="chart")
            ], className="chart-container"),
            html.Div([
                dcc.Graph(id='btc-eth-ratio-chart', className="chart")
            ], className="chart-container"),
            html.Div([
                dcc.Graph(id='xrp-chart', className="chart")
            ], className="chart-container")
        ], className="chart-row")
    ], className="dashboard-content"),
    
    # Interval component for updates
    dcc.Interval(
        id='interval-component',
        interval=UPDATE_INTERVAL_SECONDS*1000,  # in milliseconds
        n_intervals=0
    )
])

# Callback to update all charts
@app.callback(
    [Output('gold-chart', 'figure'),
     Output('silver-chart', 'figure'),
     Output('gold-silver-ratio-chart', 'figure'),
     Output('tsla-chart', 'figure'),
     Output('bitcoin-chart', 'figure'),
     Output('ethereum-chart', 'figure'),
     Output('btc-eth-ratio-chart', 'figure'),
     Output('xrp-chart', 'figure'),
     Output('update-time', 'children'),
     Output('update-status', 'children'),
     Output('update-status', 'className')],
    [Input('interval-component', 'n_intervals')]
)
def update_charts(n):
    try:
        # Generate data for each asset
        gold_df = generate_mock_data('Gold')
        silver_df = generate_mock_data('Silver')
        tsla_df = generate_mock_data('TSLA')
        btc_df = generate_mock_data('Bitcoin')
        eth_df = generate_mock_data('Ethereum')
        xrp_df = generate_mock_data('XRP')
        
        # Create ratio dataframes
        gold_silver_ratio = create_ratio_data(gold_df, silver_df, 'Gold', 'Silver')
        btc_eth_ratio = create_ratio_data(btc_df, eth_df, 'Bitcoin', 'Ethereum')
        
        # Create charts
        gold_chart = create_chart(gold_df, 'Spot Gold (per oz)', CHART_COLORS['Gold'])
        silver_chart = create_chart(silver_df, 'Spot Silver (per oz)', CHART_COLORS['Silver'])
        gold_silver_ratio_chart = create_chart(gold_silver_ratio, 'Gold/Silver Ratio', CHART_COLORS['Gold_Silver_Ratio'])
        tsla_chart = create_chart(tsla_df, 'TSLA Stock', CHART_COLORS['TSLA'])
        
        btc_chart = create_chart(btc_df, 'Bitcoin (USD)', CHART_COLORS['Bitcoin'])
        eth_chart = create_chart(eth_df, 'Ethereum (USD)', CHART_COLORS['Ethereum'])
        btc_eth_ratio_chart = create_chart(btc_eth_ratio, 'BTC/ETH Ratio', CHART_COLORS['BTC_ETH_Ratio'])
        xrp_chart = create_chart(xrp_df, 'XRP (USD)', CHART_COLORS['XRP'])
        
        # Update time
        update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        return (
            gold_chart, silver_chart, gold_silver_ratio_chart, tsla_chart,
            btc_chart, eth_chart, btc_eth_ratio_chart, xrp_chart,
            update_time, "Data Updated Successfully", "update-status success"
        )
    except Exception as e:
        # If there's an error, return the error message
        update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return (
            {}, {}, {}, {}, {}, {}, {}, {},
            update_time, f"Error: {str(e)}", "update-status error"
        )

# Run the app
if __name__ == '__main__':
    app.run(debug=DEBUG_MODE, host=SERVER_HOST, port=SERVER_PORT)
