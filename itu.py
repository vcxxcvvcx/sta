import requests
from bs4 import BeautifulSoup

def get_quarterly_net_profit(stock_code):
    url = f"https://itooza.com/stats/{stock_code}/0/32"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the table row that contains the quarterly net profit data
    net_profit_row = soup.find('tr', class_='10_13')
    
    if not net_profit_row:
        print(f"No data found for stock code {stock_code}")
        return []
    
    # Extract the net profit values from the table row
    net_profits = []
    for td in net_profit_row.find_all('td', class_='right'):
        text = td.text.strip()
        if text:  # Ensure that the text is not empty
            try:
                profit = int(text.replace(',', ''))
                net_profits.append(profit)
            except ValueError:
                continue
    
    return net_profits

def find_companies_with_3_losses_then_profit(stock_codes):
    companies_with_3_losses_then_profit = []

    for stock_code in stock_codes:
        net_profits = get_quarterly_net_profit(stock_code)
        
        if len(net_profits) < 4:
            continue
        
        # Check for 3 consecutive quarters with a negative net profit followed by a positive net profit
        for i in range(len(net_profits) - 3):
            if all(profit < 0 for profit in net_profits[i:i+3]) and net_profits[i+3] > 0:
                companies_with_3_losses_then_profit.append(stock_code)
                break

    return companies_with_3_losses_then_profit

# Example usage
stock_codes = ['267980', '114190', '86390']  # Add other stock codes as needed
companies_with_3_losses_then_profit = find_companies_with_3_losses_then_profit(stock_codes)

print("Companies with 3 or more consecutive quarterly losses followed by a profit:")
for company in companies_with_3_losses_then_profit:
    print(company)
