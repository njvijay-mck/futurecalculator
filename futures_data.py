import pandas as pd
import yfinance as yf
import numpy as np
from datetime import datetime, timedelta

# Define futures data with all required information
FUTURES_DATA = {
    "Equity": [
        {
            "name": "E-mini S&P 500",
            "symbol": "ES=F",
            "ticker": "/ES",
            "notional_value": "S&P 500 Index x $50",
            "tick_size": 0.25,
            "multiplier": 50,
            "etf_equivalent": "SPY",
            "etf_shares_approx": "~500 shares",
            "initial_margin": 12650
        },
        {
            "name": "Micro E-mini S&P 500",
            "symbol": "MES=F",
            "ticker": "/MES",
            "notional_value": "S&P 500 Index x $5",
            "tick_size": 0.25,
            "multiplier": 5,
            "etf_equivalent": "SPY",
            "etf_shares_approx": "~50 shares",
            "initial_margin": 1265
        },
        {
            "name": "E-mini Nasdaq-100",
            "symbol": "NQ=F",
            "ticker": "/NQ",
            "notional_value": "Nasdaq-100 Index x $20",
            "tick_size": 0.25,
            "multiplier": 20,
            "etf_equivalent": "QQQ",
            "etf_shares_approx": "~200 shares",
            "initial_margin": 16500
        },
        {
            "name": "Micro E-mini Nasdaq-100",
            "symbol": "MNQ=F",
            "ticker": "/MNQ",
            "notional_value": "Nasdaq-100 Index x $2",
            "tick_size": 0.25,
            "multiplier": 2,
            "etf_equivalent": "QQQ",
            "etf_shares_approx": "~20 shares",
            "initial_margin": 1650
        },
        {
            "name": "E-mini Dow",
            "symbol": "YM=F",
            "ticker": "/YM",
            "notional_value": "DJIA x $5",
            "tick_size": 1.0,
            "multiplier": 5,
            "etf_equivalent": "DIA",
            "etf_shares_approx": "~150 shares",
            "initial_margin": 10450
        },
        {
            "name": "Micro E-mini Dow",
            "symbol": "MYM=F",
            "ticker": "/MYM",
            "notional_value": "DJIA x $0.50",
            "tick_size": 1.0,
            "multiplier": 0.5,
            "etf_equivalent": "DIA",
            "etf_shares_approx": "~15 shares",
            "initial_margin": 1045
        },
        {
            "name": "E-mini Russell 2000",
            "symbol": "RTY=F",
            "ticker": "/RTY",
            "notional_value": "Russell 2000 Index x $50",
            "tick_size": 0.1,
            "multiplier": 50,
            "etf_equivalent": "IWM",
            "etf_shares_approx": "~250 shares",
            "initial_margin": 8250
        },
        {
            "name": "Micro E-mini Russell 2000",
            "symbol": "M2K=F",
            "ticker": "/M2K",
            "notional_value": "Russell 2000 Index x $5",
            "tick_size": 0.1,
            "multiplier": 5,
            "etf_equivalent": "IWM",
            "etf_shares_approx": "~25 shares",
            "initial_margin": 825
        }
    ],
    "Energy": [
        {
            "name": "Crude Oil",
            "symbol": "CL=F",
            "ticker": "/CL",
            "notional_value": "1,000 barrels",
            "tick_size": 0.01,
            "multiplier": 1000,
            "etf_equivalent": "USO",
            "etf_shares_approx": "~700 shares",
            "initial_margin": 6050
        },
        {
            "name": "Micro WTI Crude Oil",
            "symbol": "MCL=F",
            "ticker": "/MCL",
            "notional_value": "100 barrels",
            "tick_size": 0.01,
            "multiplier": 100,
            "etf_equivalent": "USO",
            "etf_shares_approx": "~70 shares",
            "initial_margin": 605
        },
        {
            "name": "Natural Gas",
            "symbol": "NG=F",
            "ticker": "/NG",
            "notional_value": "10,000 MMBtu",
            "tick_size": 0.001,
            "multiplier": 10000,
            "etf_equivalent": "UNG",
            "etf_shares_approx": "~900 shares",
            "initial_margin": 3300
        },
        {
            "name": "Micro Natural Gas",
            "symbol": "MNG=F",
            "ticker": "/MNG",
            "notional_value": "1,000 MMBtu",
            "tick_size": 0.001,
            "multiplier": 1000,
            "etf_equivalent": "UNG",
            "etf_shares_approx": "~90 shares",
            "initial_margin": 330
        }
    ],
    "Metals": [
        {
            "name": "Gold",
            "symbol": "GC=F",
            "ticker": "/GC",
            "notional_value": "100 troy ounces",
            "tick_size": 0.1,
            "multiplier": 100,
            "etf_equivalent": "GLD",
            "etf_shares_approx": "~550 shares",
            "initial_margin": 11000
        },
        {
            "name": "Micro Gold",
            "symbol": "MGC=F",
            "ticker": "/MGC",
            "notional_value": "10 troy ounces",
            "tick_size": 0.1,
            "multiplier": 10,
            "etf_equivalent": "GLD",
            "etf_shares_approx": "~55 shares",
            "initial_margin": 1100
        },
        {
            "name": "Silver",
            "symbol": "SI=F",
            "ticker": "/SI",
            "notional_value": "5,000 troy ounces",
            "tick_size": 0.005,
            "multiplier": 5000,
            "etf_equivalent": "SLV",
            "etf_shares_approx": "~1000 shares",
            "initial_margin": 9900
        },
        {
            "name": "Micro Silver",
            "symbol": "SIL=F",
            "ticker": "/SIL",
            "notional_value": "1,000 troy ounces",
            "tick_size": 0.005,
            "multiplier": 1000,
            "etf_equivalent": "SLV",
            "etf_shares_approx": "~200 shares",
            "initial_margin": 1980
        },
        {
            "name": "Copper",
            "symbol": "HG=F",
            "ticker": "/HG",
            "notional_value": "25,000 pounds",
            "tick_size": 0.0005,
            "multiplier": 25000,
            "etf_equivalent": "CPER",
            "etf_shares_approx": "~600 shares",
            "initial_margin": 7150
        }
    ],
    "Currency": [
        {
            "name": "Euro FX",
            "symbol": "6E=F",
            "ticker": "/6E",
            "notional_value": "€125,000",
            "tick_size": 0.00005,
            "multiplier": 125000,
            "etf_equivalent": "FXE",
            "etf_shares_approx": "~1100 shares",
            "initial_margin": 2750
        },
        {
            "name": "Micro E-mini Euro",
            "symbol": "M6E=F",
            "ticker": "/M6E",
            "notional_value": "€12,500",
            "tick_size": 0.00005,
            "multiplier": 12500,
            "etf_equivalent": "FXE",
            "etf_shares_approx": "~110 shares",
            "initial_margin": 275
        },
        {
            "name": "Japanese Yen",
            "symbol": "6J=F",
            "ticker": "/6J",
            "notional_value": "¥12,500,000",
            "tick_size": 0.0000005,
            "multiplier": 12500000,
            "etf_equivalent": "FXY",
            "etf_shares_approx": "~1500 shares",
            "initial_margin": 2750
        },
        {
            "name": "British Pound",
            "symbol": "6B=F",
            "ticker": "/6B",
            "notional_value": "£62,500",
            "tick_size": 0.0001,
            "multiplier": 62500,
            "etf_equivalent": "FXB",
            "etf_shares_approx": "~600 shares",
            "initial_margin": 2750
        }
    ],
    "Volatility": [
        {
            "name": "VIX Futures",
            "symbol": "VX=F",
            "ticker": "/VX",
            "notional_value": "$1,000 x VIX Index",
            "tick_size": 0.05,
            "multiplier": 1000,
            "etf_equivalent": "VXX",
            "etf_shares_approx": "~400 shares",
            "initial_margin": 8250
        },
        {
            "name": "Micro VIX Futures",
            "symbol": "VXM=F",
            "ticker": "/VXM",
            "notional_value": "$100 x VIX Index",
            "tick_size": 0.05,
            "multiplier": 100,
            "etf_equivalent": "VXX",
            "etf_shares_approx": "~40 shares",
            "initial_margin": 825
        }
    ],
    "Crypto": [
        {
            "name": "Bitcoin Futures",
            "symbol": "BTC=F",
            "ticker": "/BTC",
            "notional_value": "5 bitcoin",
            "tick_size": 5.0,
            "multiplier": 5,
            "etf_equivalent": "BITO",
            "etf_shares_approx": "~2000 shares",
            "initial_margin": 40150
        },
        {
            "name": "Micro Bitcoin Futures",
            "symbol": "MBT=F",
            "ticker": "/MBT",
            "notional_value": "0.1 bitcoin",
            "tick_size": 0.5,
            "multiplier": 0.1,
            "etf_equivalent": "BITO",
            "etf_shares_approx": "~40 shares",
            "initial_margin": 803
        },
        {
            "name": "Ethereum Futures",
            "symbol": "ETH=F",
            "ticker": "/ETH",
            "notional_value": "50 ether",
            "tick_size": 0.25,
            "multiplier": 50,
            "etf_equivalent": "ETHA",
            "etf_shares_approx": "~1500 shares",
            "initial_margin": 22000
        },
        {
            "name": "Micro Ethereum Futures",
            "symbol": "MET=F",
            "ticker": "/MET",
            "notional_value": "0.1 ether",
            "tick_size": 0.25,
            "multiplier": 0.1,
            "etf_equivalent": "ETHA",
            "etf_shares_approx": "~3 shares",
            "initial_margin": 440
        }
    ],
    "Grains": [
        {
            "name": "Corn",
            "symbol": "ZC=F",
            "ticker": "/ZC",
            "notional_value": "5,000 bushels",
            "tick_size": 0.25,
            "multiplier": 50,
            "etf_equivalent": "CORN",
            "etf_shares_approx": "~300 shares",
            "initial_margin": 2475
        },
        {
            "name": "Soybeans",
            "symbol": "ZS=F",
            "ticker": "/ZS",
            "notional_value": "5,000 bushels",
            "tick_size": 0.25,
            "multiplier": 50,
            "etf_equivalent": "SOYB",
            "etf_shares_approx": "~400 shares",
            "initial_margin": 3300
        },
        {
            "name": "Wheat",
            "symbol": "ZW=F",
            "ticker": "/ZW",
            "notional_value": "5,000 bushels",
            "tick_size": 0.25,
            "multiplier": 50,
            "etf_equivalent": "WEAT",
            "etf_shares_approx": "~350 shares",
            "initial_margin": 2750
        }
    ],
    "Livestock": [
        {
            "name": "Live Cattle",
            "symbol": "LE=F",
            "ticker": "/LE",
            "notional_value": "40,000 pounds",
            "tick_size": 0.025,
            "multiplier": 400,
            "etf_equivalent": "COW",
            "etf_shares_approx": "~200 shares",
            "initial_margin": 2200
        },
        {
            "name": "Lean Hogs",
            "symbol": "HE=F",
            "ticker": "/HE",
            "notional_value": "40,000 pounds",
            "tick_size": 0.025,
            "multiplier": 400,
            "etf_equivalent": "COW",
            "etf_shares_approx": "~200 shares",
            "initial_margin": 2200
        }
    ],
    "Treasuries": [
        {
            "name": "10-Year T-Note",
            "symbol": "ZN=F",
            "ticker": "/ZN",
            "notional_value": "$100,000 face value",
            "tick_size": 0.015625,
            "multiplier": 1000,
            "etf_equivalent": "IEF",
            "etf_shares_approx": "~900 shares",
            "initial_margin": 2750
        },
        {
            "name": "2-Year T-Note",
            "symbol": "ZT=F",
            "ticker": "/ZT",
            "notional_value": "$200,000 face value",
            "tick_size": 0.0078125,
            "multiplier": 2000,
            "etf_equivalent": "SHY",
            "etf_shares_approx": "~2300 shares",
            "initial_margin": 1100
        },
        {
            "name": "30-Year T-Bond",
            "symbol": "ZB=F",
            "ticker": "/ZB",
            "notional_value": "$100,000 face value",
            "tick_size": 0.03125,
            "multiplier": 1000,
            "etf_equivalent": "TLT",
            "etf_shares_approx": "~650 shares",
            "initial_margin": 4400
        },
        {
            "name": "Ultra T-Bond",
            "symbol": "UB=F",
            "ticker": "/UB",
            "notional_value": "$100,000 face value",
            "tick_size": 0.03125,
            "multiplier": 1000,
            "etf_equivalent": "TLT",
            "etf_shares_approx": "~700 shares",
            "initial_margin": 5500
        }
    ]
}

def get_all_futures():
    """Return a list of all futures with their details"""
    all_futures = []
    for section, futures in FUTURES_DATA.items():
        for future in futures:
            future_data = future.copy()
            future_data['section'] = section
            future_data['value_per_tick'] = future_data['tick_size'] * future_data['multiplier']
            all_futures.append(future_data)
    return all_futures

def get_all_futures_df():
    """Return a dataframe of all futures with their details"""
    return pd.DataFrame(get_all_futures())

def get_future_by_symbol(symbol):
    """Get future details by symbol"""
    all_futures = get_all_futures()
    for future in all_futures:
        if future['symbol'] == symbol:
            return future
    return None

def calculate_atr(symbol, period=14):
    """Calculate the Average True Range (ATR) for a given symbol"""
    try:
        # Get data from Yahoo Finance
        end_date = datetime.now()
        start_date = end_date - timedelta(days=period*2)  # Get more data than needed to ensure we have enough
        
        data = yf.download(symbol, start=start_date, end=end_date)
        
        if data.empty:
            return None
        
        # Calculate True Range
        data['High-Low'] = data['High'] - data['Low']
        data['High-PrevClose'] = abs(data['High'] - data['Close'].shift(1))
        data['Low-PrevClose'] = abs(data['Low'] - data['Close'].shift(1))
        
        data['TR'] = data[['High-Low', 'High-PrevClose', 'Low-PrevClose']].max(axis=1)
        
        # Calculate ATR
        data['ATR'] = data['TR'].rolling(window=period).mean()
        
        # Get the latest ATR value
        latest_atr = data['ATR'].iloc[-1]
        
        return latest_atr
    except Exception as e:
        print(f"Error calculating ATR for {symbol}: {e}")
        return None

def get_current_price(symbol):
    """Get the current price for a given symbol"""
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="1d")
        if not data.empty:
            return data['Close'].iloc[-1]
        return None
    except Exception as e:
        print(f"Error getting price for {symbol}: {e}")
        return None

def calculate_notional_exposure(future):
    """Calculate the notional exposure for a future contract"""
    price = get_current_price(future['symbol'])
    if price:
        return price * future['multiplier']
    return None

def calculate_daily_pnl_range(future):
    """Calculate the approximate daily P&L range based on ATR"""
    atr = calculate_atr(future['symbol'])
    if atr:
        return atr * future['multiplier']
    return None

def get_all_futures_with_market_data():
    """Get all futures with current market data"""
    futures = get_all_futures()
    for future in futures:
        price = get_current_price(future['symbol'])
        atr = calculate_atr(future['symbol'])
        
        if price:
            future['current_price'] = price
            future['notional_exposure'] = price * future['multiplier']
        else:
            future['current_price'] = "N/A"
            future['notional_exposure'] = "N/A"
            
        if atr:
            future['atr'] = atr
            future['daily_pnl_range'] = atr * future['multiplier']
        else:
            future['atr'] = "N/A"
            future['daily_pnl_range'] = "N/A"
            
    return futures

def get_stop_loss_levels(future, atr_multipliers=[0.5, 0.75, 1.0, 1.25, 1.5]):
    """Calculate stop loss levels based on ATR multipliers"""
    price = get_current_price(future['symbol'])
    atr = calculate_atr(future['symbol'])
    
    if not price or not atr:
        return None
    
    stop_levels = {}
    for multiplier in atr_multipliers:
        stop_distance = atr * multiplier
        stop_price = price - stop_distance  # For long position
        stop_loss_amount = stop_distance * future['multiplier']
        
        stop_levels[f"{multiplier} ATR"] = {
            "stop_price": stop_price,
            "stop_distance": stop_distance,
            "stop_loss_amount": stop_loss_amount
        }
    
    return stop_levels

def calculate_r_multiples(stop_loss_amount, r_multiples=[1, 2, 2.5, 3]):
    """Calculate R multiple targets based on stop loss amount"""
    if not stop_loss_amount or stop_loss_amount == "N/A":
        return None
    
    r_targets = {}
    for r in r_multiples:
        r_targets[f"{r}R"] = stop_loss_amount * r
    
    return r_targets
