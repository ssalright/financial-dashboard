import dash
from dash import dcc, html, callback_context
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
def generate_mock_data(asset_name, timeframe='3d'):
    """Generate realistic mock data for financial assets with mean reversion"""
    # Map timeframes to days and frequency
    timeframe_config = {
        '3d': {'days': 3, 'freq': '15min'},
        '2w': {'days': 14, 'freq': '1h'},
        '3m': {'days': 90, 'freq': '4h'},
        '1yr': {'days': 365, 'freq': '1d'},
        '5y': {'days': 1825, 'freq': '1W'},
        '10y': {'days': 3650, 'freq': '1W'}
    }
    
    config = timeframe_config.get(timeframe, timeframe_config['3d'])
    days = config['days']
    freq = config['freq']
        
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=days)
    
    # Create date range
    dates = pd.date_range(start=start_date, end=end_date, freq=freq)
    n = len(dates)
    
    # Ensure we have at least some data points
    if n == 0:
        # Fallback: create at least 24 hourly points
        dates = pd.date_range(start=start_date, periods=24, freq='h')
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
    prices = [current_price * (0.95 + 0.1 * np.random.random())]  # Start near current price
    
    for i in range(1, n):
        # Mean reversion component (much smaller to prevent exponential growth)
        mean_reversion_component = mean_reversion * (current_price - prices[-1]) / current_price
        # Random component (smaller volatility)
        random_component = volatility * np.random.normal()
        # New price (additive rather than multiplicative to prevent explosion)
        price_change = mean_reversion_component + random_component
        new_price = prices[-1] * (1 + price_change)
        # Ensure price stays within reasonable bounds
        new_price = max(new_price, 0.1 * current_price)
        new_price = min(new_price, 10 * current_price)
        prices.append(new_price)
    
    # Ensure the last price is close to the current market price
    if len(prices) > 0:
        prices[-1] = current_price * (0.98 + 0.04 * np.random.random())
    
    # Create DataFrame
    df = pd.DataFrame({
        'Date': dates[:len(prices)],  # Ensure dates and prices have same length
        'Price': prices
    })
    
    return df

# Function to create ratio data
def create_ratio_data(df1, df2, name1, name2):
    """Create ratio data from two dataframes"""
    # Check if either dataframe is empty
    if df1.empty or df2.empty or len(df1) == 0 or len(df2) == 0:
        # Return empty dataframe with correct structure
        return pd.DataFrame({'Date': [], 'Price': []})
    
    try:
        # Use the shorter dataframe's dates to ensure alignment
        min_len = min(len(df1), len(df2))
        if min_len == 0:
            return pd.DataFrame({'Date': [], 'Price': []})
            
        # Take the first min_len rows from each dataframe
        df1_subset = df1.head(min_len).copy()
        df2_subset = df2.head(min_len).copy()
        
        # Calculate ratio using the prices directly
        ratio_values = df1_subset['Price'].values / df2_subset['Price'].values
        
        # Create result dataframe
        result = pd.DataFrame({
            'Date': df1_subset['Date'].values,
            'Price': ratio_values
        })
        
        return result
    except Exception as e:
        print(f"Error creating ratio data for {name1}/{name2}: {e}")
        return pd.DataFrame({'Date': [], 'Price': []})

# Function to create a chart
def create_chart(df, title, color='#1f77b4'):
    """Create a plotly chart from dataframe"""
    fig = go.Figure()
    
    # Check if dataframe is empty
    if df.empty or len(df) == 0:
        # Create empty chart with message
        fig.add_annotation(
            x=0.5, y=0.5,
            text="No data available",
            showarrow=False,
            xref="paper", yref="paper",
            font=dict(size=16, color="gray")
        )
    else:
        fig.add_trace(go.Scatter(
            x=df['Date'],
            y=df['Price'],
            mode='lines',
            name=title,
            line=dict(color=color, width=2),
            hovertemplate='%{y:.2f}<extra></extra>'
        ))
        
        # Add current price annotation if data exists
        if len(df) > 0:
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
            linewidth=1,
            type='date'
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
    
    # Timeframe selector
    html.Div([
        html.Div([
            html.Span("Timeframe: ", className="timeframe-label"),
            html.Button("3d", id="btn-3d", className="timeframe-btn active", n_clicks=0),
            html.Button("2w", id="btn-2w", className="timeframe-btn", n_clicks=0),
            html.Button("3m", id="btn-3m", className="timeframe-btn", n_clicks=0),
            html.Button("1yr", id="btn-1yr", className="timeframe-btn", n_clicks=0),
            html.Button("5y", id="btn-5y", className="timeframe-btn", n_clicks=0),
            html.Button("10y", id="btn-10y", className="timeframe-btn", n_clicks=0)
        ], className="timeframe-controls")
    ], className="timeframe-container"),
    
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
    
    # Hidden div to store selected timeframe
    html.Div(id='selected-timeframe', children='3d', style={'display': 'none'}),
    
    # Interval component for updates
    dcc.Interval(
        id='interval-component',
        interval=UPDATE_INTERVAL_SECONDS*1000,  # in milliseconds
        n_intervals=0
    )
])

# Callback to handle timeframe selection
@app.callback(
    [Output('selected-timeframe', 'children'),
     Output('btn-3d', 'className'),
     Output('btn-2w', 'className'),
     Output('btn-3m', 'className'),
     Output('btn-1yr', 'className'),
     Output('btn-5y', 'className'),
     Output('btn-10y', 'className')],
    [Input('btn-3d', 'n_clicks'),
     Input('btn-2w', 'n_clicks'),
     Input('btn-3m', 'n_clicks'),
     Input('btn-1yr', 'n_clicks'),
     Input('btn-5y', 'n_clicks'),
     Input('btn-10y', 'n_clicks')]
)
def update_timeframe(btn_3d, btn_2w, btn_3m, btn_1yr, btn_5y, btn_10y):
    """Update selected timeframe based on button clicks"""
    ctx = callback_context
    
    if not ctx.triggered:
        # Default to 3d
        return '3d', 'timeframe-btn active', 'timeframe-btn', 'timeframe-btn', 'timeframe-btn', 'timeframe-btn', 'timeframe-btn'
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    # Reset all button classes
    classes = ['timeframe-btn'] * 6
    
    if button_id == 'btn-3d':
        classes[0] = 'timeframe-btn active'
        return '3d', *classes
    elif button_id == 'btn-2w':
        classes[1] = 'timeframe-btn active'
        return '2w', *classes
    elif button_id == 'btn-3m':
        classes[2] = 'timeframe-btn active'
        return '3m', *classes
    elif button_id == 'btn-1yr':
        classes[3] = 'timeframe-btn active'
        return '1yr', *classes
    elif button_id == 'btn-5y':
        classes[4] = 'timeframe-btn active'
        return '5y', *classes
    elif button_id == 'btn-10y':
        classes[5] = 'timeframe-btn active'
        return '10y', *classes
    
    # Default fallback
    classes[0] = 'timeframe-btn active'
    return '3d', *classes

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
    [Input('interval-component', 'n_intervals'),
     Input('selected-timeframe', 'children')]
)
def update_charts(n, timeframe):
    try:
        # Generate data for each asset with selected timeframe
        gold_df = generate_mock_data('Gold', timeframe)
        silver_df = generate_mock_data('Silver', timeframe)
        tsla_df = generate_mock_data('TSLA', timeframe)
        btc_df = generate_mock_data('Bitcoin', timeframe)
        eth_df = generate_mock_data('Ethereum', timeframe)
        xrp_df = generate_mock_data('XRP', timeframe)
        
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
