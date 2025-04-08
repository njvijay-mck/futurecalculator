# Futures Calculator

A comprehensive Streamlit application for futures traders that provides detailed information about various futures contracts and helps with position sizing calculations.

## Features

### Futures Table
- Comprehensive information about futures contracts across multiple asset classes:
  - Equity (S&P 500, Nasdaq, etc.)
  - Energy (Crude Oil, Natural Gas)
  - Metals (Gold, Silver, Copper)
  - Currency
  - Volatility
  - Crypto
  - Grains
  - Livestock
  - Treasuries
- For each contract, view:
  - Contract specifications (symbol, tick size, multiplier)
  - Current price and notional exposure
  - SPAN margin requirements (approximate)
  - ETF equivalents
  - Average daily P&L range based on ATR (in both dollar value and points)

### Position Size Calculator
- Select any futures contract
- View contract specifications and current market data
- Calculate position size based on:
  - Account size
  - Risk percentage
  - ATR-based stop loss
- User-adjustable number of contracts with risk calculation
- Analyze stop loss levels at different ATR multiples (0.25x to 1.5x)
- View profit targets based on R-multiples (1R to 3R)
- Visual representation of risk-reward scenarios for both long and short positions
- Position sizing recommendations with minimum, selected, and maximum risk options

## Installation

1. Clone this repository
2. Install the required packages:

```
pip install -r requirements.txt
```

3. Run the application:

```
streamlit run app.py
```

## Data Source

The application uses Yahoo Finance API to fetch current market data and calculate ATR values. Please note that futures quotes may be delayed and are not automatically refreshed.

## Key Features

- **Comprehensive Futures Database**: Includes detailed information on futures contracts across 9 asset classes
- **Real-time Data**: Fetches current prices and calculates ATR values using Yahoo Finance API
- **SPAN Margin Information**: Provides approximate initial margin requirements for all contracts
- **Flexible Position Sizing**: Adjust contract quantities and see the impact on risk
- **Visual Risk Analysis**: Interactive charts showing entry, stop loss, and profit targets
- **Support for Both Long and Short Positions**: Complete analysis for both trading directions
- **Customizable Stop Loss Levels**: Choose from 0.25x to 1.5x ATR for stop placement

## Requirements

- Python 3.7+
- Streamlit 1.31.0+
- Pandas 2.1.3+
- Plotly 5.18.0+
- yfinance 0.2.35+
- NumPy 1.26.3+

## Disclaimer

This tool is for educational and informational purposes only. SPAN margin requirements are approximate and may vary between brokers. Always consult your broker for actual margin requirements before trading.
