import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import talib

# Fetch stock data (e.g., Apple stock data)
stock_data = yf.download('AAPL', start='2020-01-01', end='2023-01-01')

# Calculate Short-term (50-day) and Long-term (200-day) Moving Averages
stock_data['SMA_50'] = talib.SMA(stock_data['Close'], timeperiod=50)
stock_data['SMA_200'] = talib.SMA(stock_data['Close'], timeperiod=200)

# Create Buy/Sell signals based on Moving Average Crossover Strategy
def generate_signals(data):
    signals = pd.DataFrame(index=data.index)
    signals['Price'] = data['Close']
    signals['Signal'] = 0.0
    signals['SMA_50'] = data['SMA_50']
    signals['SMA_200'] = data['SMA_200']
    
    # Buy when short-term MA crosses above long-term MA
    signals['Signal'][50:] = np.where(signals['SMA_50'][50:] > signals['SMA_200'][50:], 1.0, 0.0)
    
    # Sell when short-term MA crosses below long-term MA
    signals['Position'] = signals['Signal'].diff()
    
    return signals

# Generate trading signals
signals = generate_signals(stock_data)

# Plot the signals on the stock price chart
plt.figure(figsize=(14, 7))
plt.plot(stock_data['Close'], label='Stock Price', color='blue', alpha=0.5)
plt.plot(stock_data['SMA_50'], label='50-day SMA', color='green', linestyle='--')
plt.plot(stock_data['SMA_200'], label='200-day SMA', color='red', linestyle='--')

# Plot Buy signals
plt.plot(signals[signals['Position'] == 1.0].index, 
         signals['SMA_50'][signals['Position'] == 1.0], 
         '^', markersize=10, color='g', lw=0, label='Buy Signal')

# Plot Sell signals
plt.plot(signals[signals['Position'] == -1.0].index, 
         signals['SMA_50'][signals['Position'] == -1.0], 
         'v', markersize=10, color='r', lw=0, label='Sell Signal')

plt.title('Moving Average Crossover Strategy')
plt.legend(loc='best')
plt.show()
