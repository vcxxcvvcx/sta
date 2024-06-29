import pandas as pd
import FinanceDataReader as fdr
from tqdm import tqdm
import matplotlib.pyplot as plt
from itertools import combinations

# Define the list of stock tickers
stock_tickers = {
    "삼성전자": "005930",
    "SK하이닉스": "000660",
    "DB하이텍": "000990",
    "원익IPS": "240810"
}

# Get historical data for the last 2 weeks
end_date = pd.to_datetime("today")
start_date = end_date - pd.DateOffset(months=3)

# Download stock data
stock_data = pd.DataFrame()
for name, ticker in stock_tickers.items():
    stock_data[name] = fdr.DataReader(ticker, start_date, end_date)['Close']

# Calculate daily returns
daily_returns = stock_data.pct_change().dropna()

# Calculate correlation matrix
correlation_matrix = daily_returns.corr()

# Initialize an empty list to store correlation pairs
correlation_pairs = []

# Iterate through combinations with progress bar
for (name1, name2) in tqdm(combinations(stock_tickers.keys(), 2), total=len(stock_tickers) * (len(stock_tickers) - 1) // 2):
    corr_value = correlation_matrix.loc[name1, name2]
    pair = (name1, name2, corr_value)
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

    # Plot the rolling correlation
    plt.figure(figsize=(14, 7))
    plt.plot(rolling_corr, label=f'Rolling Correlation ({stock_1} vs {stock_2})', color='blue')
    plt.axhline(y=0, color='gray', linestyle='--')
    plt.axhline(y=0.8, color='red', linestyle='--', label='Threshold 0.8')
    plt.axhline(y=-0.8, color='red', linestyle='--', label='Threshold -0.8')
    plt.title(f'Rolling Correlation between {stock_1} and {stock_2}')
    plt.xlabel('Date')
    plt.ylabel('Correlation')
    plt.legend()
    plt.show()
else:
    print("No pairs found with correlation above 0.8.")

