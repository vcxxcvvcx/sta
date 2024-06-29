import pandas as pd
import FinanceDataReader as fdr
from tqdm import tqdm
import matplotlib.pyplot as plt

# Define the list of stock tickers
stock_tickers = {
    "삼성전자": "005930",
    "SK하이닉스": "000660",
    "DB하이텍": "000990",
    "원익IPS": "240810"
}

# Define the KOSPI 200 ticker
kospi200_ticker = "KS200"

# Get historical data for the last 3 months
end_date = pd.to_datetime("today")
start_date = end_date - pd.DateOffset(months=3)

# Download stock data
stock_data = pd.DataFrame()
for name, ticker in stock_tickers.items():
    stock_data[name] = fdr.DataReader(ticker, start_date, end_date)['Close']

# Download KOSPI 200 data
kospi200_data = fdr.DataReader(kospi200_ticker, start_date, end_date)['Close']
stock_data['KOSPI 200'] = kospi200_data

# Calculate daily returns
daily_returns = stock_data.pct_change().dropna()

# Calculate correlation matrix
correlation_matrix = daily_returns.corr()

# Initialize an empty list to store correlation pairs
correlation_pairs = []

# Iterate through combinations with progress bar
for name in tqdm(stock_tickers.keys(), total=len(stock_tickers)):
    corr_value = correlation_matrix.loc[name, 'KOSPI 200']
    pair = (name, 'KOSPI 200', corr_value)
    correlation_pairs.append(pair)

# Sort pairs by correlation value
correlation_pairs = sorted(correlation_pairs, key=lambda x: x[2], reverse=True)

# Display the pairs
for pair in correlation_pairs:
    print(f"Pair: {pair[0]} - {pair[1]}, Correlation: {pair[2]:.2f}")

# Analyze rolling correlation for the top pair
if correlation_pairs:
    top_pair = correlation_pairs[0]
    stock_1 = top_pair[0]
    stock_2 = top_pair[1]

    print(f"\nTop Pair: {stock_1} - {stock_2}, Correlation: {top_pair[2]:.2f}")

    # Calculate rolling correlations
    window_size = 5  # 5-day rolling window
    rolling_corr = daily_returns[stock_1].rolling(window=window_size).corr(daily_returns[stock_2])

    # Plot the stock prices and rolling correlation
    fig, ax1 = plt.subplots(figsize=(14, 7))

    # Plot stock prices on ax1
    ax1.set_xlabel('Date')
    ax1.set_ylabel(f'{stock_1} Price', color='blue')
    ax1.plot(stock_data.index, stock_data[stock_1], label=f'{stock_1} Price', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')

    # Create a second y-axis for KOSPI 200
    ax3 = ax1.twinx()
    ax3.set_ylabel('KOSPI 200 Price', color='green')
    ax3.plot(stock_data.index, stock_data['KOSPI 200'], label='KOSPI 200 Price', color='green')
    ax3.tick_params(axis='y', labelcolor='green')

    # Create a third y-axis for the correlation
    ax2 = ax1.twinx()
    ax2.spines["right"].set_position(("outward", 60))
    ax2.set_ylabel('Correlation', color='red')
    ax2.plot(rolling_corr.index, rolling_corr, label=f'Rolling Correlation ({stock_1} vs KOSPI 200)', color='red')
    ax2.axhline(y=0, color='gray', linestyle='--')
    ax2.axhline(y=0.8, color='red', linestyle='--', label='Threshold 0.8')
    ax2.axhline(y=-0.8, color='red', linestyle='--', label='Threshold -0.8')
    ax2.tick_params(axis='y', labelcolor='red')

    # Add legends
    fig.legend(loc="upper left", bbox_to_anchor=(0.1, 0.9))
    plt.title(f'Price and Rolling Correlation between {stock_1} and KOSPI 200')
    fig.tight_layout()
    plt.show()
else:
    print("No pairs found with correlation above 0.8.")
