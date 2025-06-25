# Financial Assets Dashboard

A comprehensive real-time financial dashboard built with Python Dash for tracking and analyzing multiple asset classes including precious metals, stocks, and cryptocurrencies.

![Dashboard Preview](https://img.shields.io/badge/Status-Active-green) ![Python](https://img.shields.io/badge/Python-3.8+-blue) ![Dash](https://img.shields.io/badge/Dash-2.0+-orange)

## 🚀 Features

### Multi-Asset Tracking
- **Precious Metals**: Gold, Silver
- **Stocks**: Tesla (TSLA)
- **Cryptocurrencies**: Bitcoin, Ethereum, XRP

### Interactive Time Periods
- **3 Days** (15-minute intervals) - Default
- **2 Weeks** (1-hour intervals)
- **3 Months** (4-hour intervals)
- **1 Year** (daily intervals)
- **5 Years** (weekly intervals)
- **10 Years** (weekly intervals)

### Advanced Analytics
- **Price Charts**: Real-time price movements with trend analysis
- **Ratio Analysis**: Asset correlation and relative performance
- **Portfolio Metrics**: Comprehensive performance indicators
- **Risk Assessment**: Volatility and risk metrics

### User Experience
- **Global Timeframe Selector**: Single control for all charts
- **Responsive Design**: Works on desktop and mobile
- **Real-time Updates**: Live data refresh every 30 seconds
- **Interactive Charts**: Zoom, pan, and hover for detailed information

## 📊 Current Market Prices (June 25, 2025)

| Asset | Price | Symbol |
|-------|-------|--------|
| Gold | $3,330/oz | XAU |
| Silver | $35.90/oz | XAG |
| Tesla | $324.00 | TSLA |
| Bitcoin | $107,000 | BTC |
| Ethereum | $2,400 | ETH |
| XRP | $2.18 | XRP |

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/ssalright/financial-dashboard.git
   cd financial-dashboard
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the dashboard**
   ```bash
   python run_dashboard.py
   ```

4. **Access the dashboard**
   - Open your browser to `http://localhost:8888`
   - The dashboard will automatically load with 3-day timeframe selected

### Alternative Launch Methods

**Direct Python execution:**
```bash
python financial_dashboard.py
```

**Custom port:**
```bash
# Edit config.py to change SERVER_PORT
python financial_dashboard.py
```

## 📁 Project Structure

```
financial-dashboard/
├── financial_dashboard.py    # Main dashboard application
├── config.py                # Configuration settings
├── style.css               # Custom styling
├── run_dashboard.py        # Launcher script
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── .gitignore            # Git ignore rules
```

## 🚦 Usage

### Timeframe Selection
1. Use the buttons in the header to select your desired timeframe
2. All charts will automatically update to show data for the selected period
3. The active timeframe button is highlighted in blue

### Chart Interaction
- **Zoom**: Click and drag to zoom into specific time periods
- **Pan**: Hold shift and drag to pan across the chart
- **Hover**: Hover over data points for detailed information
- **Reset**: Double-click to reset zoom level

### Understanding the Data
- **Price Charts**: Show absolute price movements over time
- **Ratio Charts**: Display relative performance between assets
- **Portfolio Metrics**: Provide comprehensive performance analysis

## ⚙️ Configuration

### Server Settings (`config.py`)
```python
SERVER_HOST = '0.0.0.0'      # Server host
SERVER_PORT = 8888           # Server port
DEBUG_MODE = True            # Debug mode
DASHBOARD_TITLE = "Financial Assets Dashboard"
```

### Asset Configuration
- **Current Prices**: Updated to June 25, 2025 market values
- **Volatility Parameters**: Realistic volatility for each asset class
- **Mean Reversion**: Smart price movement simulation

## 🔧 Technical Details

### Data Generation
- **Realistic Price Movements**: Uses mean reversion with appropriate volatility
- **Multiple Timeframes**: Different data frequencies for each time period
- **Error Handling**: Robust fallback mechanisms for data generation
- **Performance Optimized**: Efficient data structures and calculations

### Chart Features
- **Plotly Integration**: Interactive, professional-grade charts
- **Responsive Layout**: Adapts to different screen sizes
- **Real-time Updates**: Automatic data refresh
- **Synchronized Navigation**: All charts update together

### Architecture
- **Modular Design**: Separated concerns for maintainability
- **Callback System**: Efficient state management
- **Error Recovery**: Graceful handling of edge cases
- **CORS Enabled**: Cross-origin resource sharing support

## 🔍 Troubleshooting

### Common Issues

**Port Already in Use**
```bash
# Check what's using the port
netstat -tlnp | grep 8888
# Or change the port in config.py
```

**Missing Dependencies**
```bash
# Reinstall requirements
pip install -r requirements.txt --force-reinstall
```

**Data Loading Issues**
- Check internet connection for real-time data
- Verify all dependencies are installed correctly
- Check console for error messages

### Performance Tips
- Use shorter timeframes (3d, 2w) for faster loading
- Close other browser tabs to free up memory
- Refresh the page if charts become unresponsive

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guidelines
- Add comments for complex logic
- Test all timeframe combinations
- Ensure responsive design compatibility

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Plotly Dash** - For the excellent dashboard framework
- **Pandas** - For powerful data manipulation capabilities
- **NumPy** - For efficient numerical computations
- **Flask-CORS** - For cross-origin resource sharing

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/ssalright/financial-dashboard/issues) page
2. Create a new issue with detailed description
3. Include error messages and system information

## 🔮 Future Enhancements

- [ ] Real-time data integration with financial APIs
- [ ] Additional asset classes (commodities, forex, bonds)
- [ ] Advanced technical indicators (RSI, MACD, Bollinger Bands)
- [ ] Portfolio optimization tools
- [ ] Export functionality (PDF, CSV)
- [ ] User authentication and personalized dashboards
- [ ] Mobile app version
- [ ] Alert system for price movements

---

**Built with ❤️ for financial analysis and data visualization**