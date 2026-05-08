import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd

# Create input field for our desired stock
# stock = input("Stock name: ")+".OL"
stock = "SATS.OL"

# Retrieve stock data frame (df) from yfinance API at an interval of 1d
df = yf.download(tickers=stock, period='1y', interval='1d')

print(df)

if df.empty:
    print(f"Data for {stock} ble ikke funnet.")
    
# Extract the volume, stock prices, and dates
volumes = df["Volume"].values.astype(int)
stock_prices = df["Close"].values
dates = df.index

# Get yesterday's volume 
volume_today = volumes[-1][0]
# volume_today = volumes[-1]


# Get the volumes for the past days (all except the last one)
volume_past_days = volumes[:-1]

# Calculate the first and third quartiles (Q1 and Q3)
Q1 = np.percentile(volume_past_days, 25)
Q3 = np.percentile(volume_past_days, 75)

# Calculate the Interquartile Range (IQR)
IQR = Q3 - Q1

# Define the lower and upper bounds for identifying outliers
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Remove outliers: volumes that are outside the bounds
filtered_volumes = [vol for vol in volume_past_days if lower_bound <= vol <= upper_bound]

# Sort the remaining volumes
filtered_volumes.sort()

# Remove the 10 lowest and 10 highest volumes from the sorted list
trimmed_volumes = np.array(filtered_volumes[10:-10])

# Calculate the mean volume of the trimmed volumes
mean_value = trimmed_volumes.mean()
mean = round(volume_today / mean_value, 2)

# ----- RSI Calculation -----
def calculate_rsi(data, period=14):
    delta = data.diff()
    gain = delta.where(delta > 0, 0).rolling(window=period).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

df['RSI'] = calculate_rsi(df['Close'])

# Print out volume and ratio
print(dates[-1])
print(f"RSI: {int(df['RSI'].iloc[-1])}")
print(f"Volume: {volume_today}")
print(f"Ratio of Volume to the Mean: {mean}")
print(f"Trimmed Mean Volume (without IQR outliers): {round(mean_value,2)}")

# Create a figure with three subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True, gridspec_kw={'height_ratios': [2, 1]})

# Plot volume
# Plot the first subplot (volume)
ax1.set_xlabel('Date')
ax1.set_ylabel('Volume', color='blue')
ax1.plot(dates, volumes, label='Volume', color='blue')
ax1.axhline(y=mean_value, color='red', linestyle='--', label=f'Mean Volume (Trimmed with IQR)')
ax1.tick_params(axis='y', labelcolor='blue')
ax1.legend(loc='upper left')

# Create a second y-axis for the stock price plot
ax1 = ax1.twinx()
ax1.set_ylabel('Stock Price', color='green')
ax1.plot(dates, stock_prices, label='Stock Price', color='green')
ax1.tick_params(axis='y', labelcolor='green')
ax1.legend(loc='upper right')

# Plot RSI
ax2.plot(dates, df['RSI'], label='RSI', color='purple')
ax2.axhline(y=70, color='red', linestyle='--', label='Overbought (70)')
ax2.axhline(y=30, color='blue', linestyle='--', label='Oversold (30)')
ax2.set_ylabel('RSI')
ax2.set_xlabel('Date')
ax2.legend(loc='upper left')

# Rotate x-axis labels
plt.xticks(rotation=45)

# Add a title
plt.suptitle(f"Stock Analysis for {stock}", fontsize=16)

# Adjust layout
plt.tight_layout(rect=[0, 0, 1, 0.97])
plt.show()