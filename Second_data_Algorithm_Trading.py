import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import talib

# Fetch stock data 
stock_data = yf.download('TSLA', start='2020-01-01', end='2023-01-01')

# Calculate RSI 
stock_data['RSI'] = talib.RSI(stock_data['Close'], timeperiod=14)

# Create Buy/Sell signals based on RSI levels
def generate_rsi_signals(data):
    signals = pd.DataFrame(index=data.index)
    signals['Price'] = data['Close']
    signals['RSI'] = data['RSI']
    signals['Signal'] = 0.0
    
    # Buy when RSI crosses above 30 (oversold)
    signals['Signal'][data['RSI'] < 30] = 1.0
    
    # Sell when RSI crosses below 70 (overbought)
    signals['Signal'][data['RSI'] > 70] = -1.0
    
    # Track the positions (buy/sell points)
    signals['Position'] = signals['Signal'].diff()
    
    return signals

# Generate trading signals
rsi_signals = generate_rsi_signals(stock_data)

# Plot the stock price and RSI with Buy/Sell signals
fig, (ax1, ax2) = plt.subplots(2, figsize=(14, 10), sharex=True)

# Plot stock price
ax1.plot(stock_data['Close'], label='Stock Price', color='blue', alpha=0.5)
ax1.set_title('RSI Trading Strategy')
ax1.set_ylabel('Stock Price')
ax1.legend(loc='best')

# Plot RSI and signals
ax2.plot(stock_data['RSI'], label='RSI', color='orange')
ax2.axhline(30, color='green', linestyle='--', label='Oversold (Buy)')
ax2.axhline(70, color='red', linestyle='--', label='Overbought (Sell)')
ax2.set_ylabel('RSI')
ax2.set_xlabel('Date')
ax2.legend(loc='best')

# Plot Buy signals
ax1.plot(rsi_signals[rsi_signals['Position'] == 1.0].index, 
         stock_data['Close'][rsi_signals['Position'] == 1.0], 
         '^', markersize=10, color='g', lw=0, label='Buy Signal')

# Plot Sell signals
ax1.plot(rsi_signals[rsi_signals['Position'] == -1.0].index, 
         stock_data['Close'][rsi_signals['Position'] == -1.0], 
         'v', markersize=10, color='r', lw=0, label='Sell Signal')

plt.show()
