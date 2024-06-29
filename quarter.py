import yfinance as yf
import pandas as pd
from tqdm import tqdm

# 코스피 200 티커 리스트
kospi_200_tickers = [
    "005930.KS", "000660.KS", "051910.KS", "035420.KS", "005380.KS", "012330.KS", 
    "005490.KS", "068270.KS", "051900.KS", "006400.KS", "017670.KS", "000270.KS", 
    "035720.KS", "036570.KS", "034730.KS", "105560.KS", "066570.KS", "028260.KS", 
    "096770.KS", "018260.KS", "090430.KS", "032830.KS", "377300.KS", "003550.KS", 
    "015760.KS", "011070.KS", "055550.KS", "086790.KS", "018880.KS", "010130.KS", 
    "030200.KS", "010140.KS", "009150.KS", "011780.KS", "010620.KS", "000810.KS", 
    "000720.KS", "009830.KS", "001040.KS", "003620.KS", "004020.KS", "004800.KS", 
    "000100.KS", "003490.KS", "000990.KS", "003410.KS", "010060.KS", "035250.KS", 
    "010950.KS", "002790.KS", "011170.KS", "005940.KS", "012750.KS", "001450.KS", 
    "001740.KS", "002790.KS", "000120.KS", "008560.KS", "008350.KS", "004990.KS", 
    "009240.KS", "012510.KS", "000210.KS", "010690.KS", "004940.KS", "025540.KS", 
    "000320.KS", "001800.KS", "005440.KS", "000040.KS", "034020.KS", "001520.KS", 
    "010120.KS", "004370.KS", "004000.KS", "002380.KS", "001630.KS", "009190.KS", 
    "005110.KS", "000080.KS", "069620.KS", "011420.KS", "035510.KS", "069960.KS", 
    "005830.KS", "007310.KS", "003070.KS", "003600.KS", "003720.KS", "003090.KS", 
    "003480.KS", "001020.KS", "001060.KS", "000400.KS", "000480.KS", "005870.KS", 
    "002710.KS", "003850.KS", "008770.KS", "002870.KS", "010600.KS", "004410.KS", 
    "002900.KS", "006390.KS", "003540.KS", "006570.KS", "014680.KS", "002990.KS", 
    "004540.KS", "005950.KS", "005710.KS", "010050.KS", "000060.KS", "017180.KS", 
    "000050.KS", "015540.KS", "010780.KS", "002240.KS", "013580.KS", "001430.KS", 
    "016610.KS", "005850.KS", "002350.KS", "004490.KS", "004170.KS", "001550.KS", 
    "005180.KS", "006260.KS", "006280.KS", "016360.KS", "005430.KS", "005880.KS", 
    "000590.KS", "008250.KS", "003300.KS", "000220.KS", "012320.KS", "003460.KS", 
    "012800.KS", "016090.KS", "008000.KS", "002820.KS", "008600.KS", "012200.KS", 
    "004170.KS", "000390.KS", "003690.KS", "000230.KS", "005720.KS", "005820.KS", 
    "003080.KS", "010040.KS", "009420.KS", "000720.KS", "000950.KS", "001420.KS", 
    "006380.KS", "006360.KS", "004690.KS", "011000.KS", "010240.KS", "011790.KS", 
    "010130.KS", "009770.KS", "004140.KS", "004490.KS", "003560.KS", "005090.KS", 
    "002700.KS", "004060.KS", "002150.KS", "002960.KS", "001680.KS", "011160.KS", 
    "001120.KS", "004450.KS", "008490.KS", "005320.KS", "002840.KS", "001250.KS", 
    "001530.KS", "006740.KS", "000910.KS", "005610.KS", "004650.KS", "009470.KS", 
    "004270.KS", "005610.KS", "010820.KS", "002370.KS", "003490.KS", "000970.KS"
]

# 적자였다가 흑자로 전환한 기업을 저장할 리스트
profitable_companies = []

# tqdm을 사용하여 진행 상황 표시
for ticker in tqdm(kospi_200_tickers, desc="Processing KOSPI 200 Tickers"):
    stock = yf.Ticker(ticker)
    
    try:
        # 재무 데이터 (분기별 손익계산서) 가져오기
        income_statement = stock.quarterly_financials.T
        income_statement = income_statement.reset_index()
        
        # 필요한 열만 선택
        income_statement = income_statement[['index', 'Net Income']]
        
        # 최근 8분기간의 데이터만 선택
        recent_12_quarters = income_statement.tail(8)
        
        # 순이익 데이터 추출
        net_incomes = recent_12_quarters['Net Income'].apply(pd.to_numeric, errors='coerce').fillna(0).values
        
        # 데이터를 확인하기 위해 출력
        print(f"Ticker: {ticker}")
        print(recent_12_quarters)
        
        # 4분기 이상 연속으로 적자였다가 흑자로 전환 여부 확인
        consecutive_losses = 0
        turned_profitable = False
        
        for i in range(len(net_incomes) - 1):
            if net_incomes[i] < 0:
                consecutive_losses += 1
            else:
                consecutive_losses = 0
                
            if consecutive_losses >= 4 and net_incomes[i+1] > 0:
                turned_profitable = True
                break

        if turned_profitable:
            profitable_companies.append(ticker)
    
    except Exception as e:
        print(f"Error processing {ticker}: {e}")

# 결과 데이터프레임으로 변환
result_df = pd.DataFrame(profitable_companies, columns=['Ticker'])

# 결과 출력
print("4분기 이상 연속으로 적자였다가 흑자로 전환한 기업:")
print(result_df)
