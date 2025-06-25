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
```bash
python financial_dashboard.py
```

4. Open your browser and navigate to `http://localhost:12000`

## Usage

The dashboard will automatically start displaying financial data with the following features:

- **Live Updates**: Data refreshes every 20 seconds
- **Interactive Charts**: Click and drag to zoom, hover for detailed values
- **Current Prices**: Latest prices are annotated on each chart
- **Status Indicator**: Shows last update time and status in the header

## Configuration

### Customizing Assets
To modify the assets being tracked, edit the `CURRENT_PRICES` dictionary in `financial_dashboard.py`:

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

### Adjusting Update Frequency
Change the update interval by modifying the `interval` parameter in the `dcc.Interval` component:

```python
dcc.Interval(
    id='interval-component',
    interval=20*1000,  # in milliseconds (20 seconds)
    n_intervals=0
)
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
├── assets/
│   └── style.css            # Custom styling
├── requirements.txt         # Python dependencies
└── README.md               # This file
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