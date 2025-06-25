"""
Configuration file for the Financial Dashboard.
Modify these settings to customize the dashboard behavior.
"""

# Server Configuration
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 12001
DEBUG_MODE = True

# Dashboard Configuration
DASHBOARD_TITLE = "Financial Assets Dashboard"
UPDATE_INTERVAL_SECONDS = 20  # How often to refresh data

# Asset Configuration - Current market prices (as of June 25, 2025 11:34am NY timezone)
CURRENT_PRICES = {
    'Gold': 3330,      # USD per ounce
    'Silver': 35.9,    # USD per ounce
    'TSLA': 324,       # USD per share
    'Bitcoin': 107000, # USD per BTC
    'Ethereum': 2400,  # USD per ETH
    'XRP': 2.18        # USD per XRP
}

# Chart Configuration
CHART_COLORS = {
    'Gold': '#FFD700',
    'Silver': '#C0C0C0',
    'Gold_Silver_Ratio': '#B87333',
    'TSLA': '#E31937',
    'Bitcoin': '#F7931A',
    'Ethereum': '#627EEA',
    'BTC_ETH_Ratio': '#8A2BE2',
    'XRP': '#23292F'
}

# Data Generation Parameters
VOLATILITY_PARAMS = {
    'Gold': {'volatility': 0.008, 'mean_reversion': 0.02},
    'Silver': {'volatility': 0.015, 'mean_reversion': 0.03},
    'TSLA': {'volatility': 0.025, 'mean_reversion': 0.01},
    'Bitcoin': {'volatility': 0.03, 'mean_reversion': 0.015},
    'Ethereum': {'volatility': 0.035, 'mean_reversion': 0.02},
    'XRP': {'volatility': 0.025, 'mean_reversion': 0.02}
}

# Historical Data Configuration
HISTORICAL_DAYS = 30  # Number of days of historical data to generate
DATA_FREQUENCY = 'h'  # Data frequency: 'h' for hourly, 'D' for daily, '15min' for 15-minute intervals