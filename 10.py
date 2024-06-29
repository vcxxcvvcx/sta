import pandas as pd
import FinanceDataReader as fdr

# Define the KOSDAQ 150 ticker list (example subset)
kosdaq_150_tickers = {
    "카카오게임즈": "293490",
    "원익IPS": "240810",
    "주성엔지니어링": "036930",
    "LS머트리얼즈": "299660",
    "파마리서치": "214450",
    "PSK홀딩스": "031980",
    "도쿄일렉트론코리아": "064760",
    "솔브레인홀딩스": "036830",
    # The list should be expanded with all 150 tickers
}

# Define the date range for the past 10 quarters (approximately 2.5 years)
end_date = pd.to_datetime("today")
start_date = end_date - pd.DateOffset(years=2.5)

# Function to check quarterly financial data
def check_financial_conditions(ticker):
    # Fetch quarterly financial data
    financials = fdr.DataReader(ticker, start=start_date, end=end_date, data_source='financials')
    
    # Check for at least 10 quarters of data
    if len(financials) < 10:
        return False, None
    
    # Extract net income data for the past 10 quarters
    net_income = financials['NetIncome'].iloc[-10:]
    
    # Check the conditions: 8 consecutive losses followed by 2 increasing profits
    if (net_income.iloc[:8] < 0).all() and net_income.iloc[8] > 0 and net_income.iloc[9] > net_income.iloc[8]:
        return True, financials.index[-10:]
    
    return False, None

# List to store the results
results = []

# Check each KOSDAQ 150 company
for name, ticker in kosdaq_150_tickers.items():
    meets_conditions, dates = check_financial_conditions(ticker)
    if meets_conditions:
        results.append((name, ticker, dates))

# Display the results
for result in results:
    name, ticker, dates = result
    print(f"기업명: {name}, 티커: {ticker}, 기간: {dates}")
