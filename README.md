# Financial Dashboard

A real-time financial assets dashboard built with Dash and Plotly, displaying live price data for various financial instruments including precious metals, stocks, and cryptocurrencies.

## Features

- **Real-time Price Tracking**: Monitor current prices for Gold, Silver, Tesla (TSLA), Bitcoin, Ethereum, and XRP
- **Interactive Charts**: Responsive charts with hover details and zoom functionality
- **Asset Ratios**: Track important ratios like Gold/Silver and BTC/ETH
- **Auto-refresh**: Dashboard updates every 20 seconds with new data
- **Responsive Design**: Mobile-friendly layout that adapts to different screen sizes
- **Modern UI**: Clean, professional interface with smooth animations

## Assets Tracked

### Precious Metals
- **Gold** - Spot price per ounce
- **Silver** - Spot price per ounce
- **Gold/Silver Ratio** - Traditional precious metals ratio

### Stocks
- **Tesla (TSLA)** - Stock price

### Cryptocurrencies
- **Bitcoin (BTC)** - Price in USD
- **Ethereum (ETH)** - Price in USD
- **XRP** - Price in USD
- **BTC/ETH Ratio** - Cryptocurrency ratio

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ssalright/financial-dashboard.git
cd financial-dashboard
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:

**Option A: Using the launcher script (recommended)**
```bash
python run_dashboard.py
```

**Option B: Direct execution**
```bash
python financial_dashboard.py
```

4. Open your browser and navigate to `http://localhost:12001`

## Usage

The dashboard will automatically start displaying financial data with the following features:

- **Live Updates**: Data refreshes every 20 seconds
- **Interactive Charts**: Click and drag to zoom, hover for detailed values
- **Current Prices**: Latest prices are annotated on each chart
- **Status Indicator**: Shows last update time and status in the header

## Configuration

The dashboard can be easily customized by editing the `config.py` file:

### Server Settings
```python
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 12001
DEBUG_MODE = True
```

### Dashboard Settings
```python
DASHBOARD_TITLE = "Financial Assets Dashboard"
UPDATE_INTERVAL_SECONDS = 20  # How often to refresh data
```

### Asset Prices
```python
CURRENT_PRICES = {
    'Gold': 3200,      # USD per ounce
    'Silver': 37,      # USD per ounce
    'TSLA': 280,       # USD per share
    'Bitcoin': 105000, # USD per BTC
    'Ethereum': 5800,  # USD per ETH
    'XRP': 1.25        # USD per XRP
}
```

### Chart Colors
```python
CHART_COLORS = {
    'Gold': '#FFD700',
    'Silver': '#C0C0C0',
    'TSLA': '#E31937',
    'Bitcoin': '#F7931A',
    'Ethereum': '#627EEA',
    'XRP': '#23292F'
}
```

### Data Generation Parameters
```python
VOLATILITY_PARAMS = {
    'Gold': {'volatility': 0.008, 'mean_reversion': 0.02},
    'Silver': {'volatility': 0.015, 'mean_reversion': 0.03},
    # ... more assets
}
```

## Technical Details

### Architecture
- **Frontend**: Dash (React-based) with Plotly charts
- **Backend**: Flask server with CORS enabled
- **Data**: Mock data generation with realistic price movements
- **Styling**: Custom CSS with responsive design

### Data Generation
The application uses sophisticated mock data generation that includes:
- Mean reversion modeling
- Asset-specific volatility parameters
- Realistic price movements
- Current market price anchoring

### Performance
- Efficient data generation and caching
- Optimized chart rendering
- Responsive design for various screen sizes
- Error handling and status reporting

## Development

### Project Structure
```
financial-dashboard/
├── financial_dashboard.py    # Main application file
├── config.py                # Configuration settings
├── run_dashboard.py         # Launcher script
├── assets/
│   └── style.css            # Custom styling
├── requirements.txt         # Python dependencies
├── README.md               # This file
├── LICENSE                 # MIT License
└── .gitignore             # Git ignore rules
```

### Adding New Assets
1. Add the asset to `CURRENT_PRICES`
2. Create data generation parameters in `generate_mock_data()`
3. Add chart creation in the callback function
4. Update the layout to include the new chart

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## License

This project is open source and available under the [MIT License](LICENSE).

## Disclaimer

This dashboard uses mock data for demonstration purposes. For production use with real financial data, integrate with actual financial data APIs such as:
- Alpha Vantage
- Yahoo Finance API
- CoinGecko API
- Financial Modeling Prep

**Important**: This tool is for educational and demonstration purposes only. Do not use this data for actual trading or investment decisions.