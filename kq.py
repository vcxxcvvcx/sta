import yfinance as yf
import pandas as pd
from tqdm import tqdm

# 코스닥 150 티커 리스트
kosdaq_150_tickers = [
    "095570.KQ", "041510.KQ", "034730.KQ", "035900.KQ", "096770.KQ", "053800.KQ", 
    "051910.KQ", "041960.KQ", "108320.KQ", "024110.KQ", "293490.KQ", "251270.KQ", 
    "066970.KQ", "086900.KQ", "036570.KQ", "263750.KQ", "036490.KQ", "046890.KQ", 
    "089980.KQ", "035200.KQ", "243840.KQ", "141080.KQ", "247540.KQ", "097950.KQ", 
    "317770.KQ", "114450.KQ", "091990.KQ", "263800.KQ", "067160.KQ", "064550.KQ", 
    "128940.KQ", "227950.KQ", "138080.KQ", "230240.KQ", "036640.KQ", "214150.KQ", 
    "018880.KQ", "036120.KQ", "195940.KQ", "069080.KQ", "078340.KQ", "051900.KQ", 
    "035760.KQ", "194480.KQ", "057050.KQ", "067310.KQ", "043260.KQ", "109860.KQ", 
    "049950.KQ", "122310.KQ", "073070.KQ", "067900.KQ", "122640.KQ", "066430.KQ", 
    "074600.KQ", "065770.KQ", "214370.KQ", "065690.KQ", "131970.KQ", "115450.KQ", 
    "178320.KQ", "069110.KQ", "090460.KQ", "207760.KQ", "228760.KQ", "115530.KQ", 
    "083310.KQ", "115310.KQ", "036620.KQ", "121800.KQ", "089530.KQ", "950210.KQ", 
    "086390.KQ", "200230.KQ", "065350.KQ", "101160.KQ", "049180.KQ", "064760.KQ", 
    "093370.KQ", "033290.KQ", "084650.KQ", "084850.KQ", "058610.KQ", "099320.KQ", 
    "091700.KQ", "048410.KQ", "084110.KQ", "067160.KQ", "052020.KQ", "092040.KQ", 
    "054180.KQ", "096640.KQ", "038500.KQ", "131180.KQ", "088130.KQ", "178320.KQ", 
    "086450.KQ", "046310.KQ", "108230.KQ", "054050.KQ", "054620.KQ", "092600.KQ", 
    "065440.KQ", "046890.KQ", "054540.KQ", "054780.KQ", "054940.KQ", "064550.KQ", 
    "108320.KQ", "065530.KQ", "064850.KQ", "050540.KQ", "064520.KQ", "060720.KQ", 
    "078590.KQ", "068940.KQ", "072520.KQ", "078160.KQ", "094360.KQ", "067920.KQ", 
    "073110.KQ", "084010.KQ", "084990.KQ", "086890.KQ", "083450.KQ", "089970.KQ", 
    "036420.KQ", "084680.KQ", "097800.KQ", "049960.KQ", "042500.KQ", "051360.KQ", 
    "043710.KQ", "089970.KQ", "090470.KQ", "073640.KQ", "067280.KQ", "094820.KQ", 
    "092190.KQ", "087010.KQ", "036800.KQ", "067570.KQ", "095190.KQ", "068790.KQ", 
    "048470.KQ", "037760.KQ", "069920.KQ", "078070.KQ", "049960.KQ", "054630.KQ"
]

# 적자였다가 흑자로 전환한 기업을 저장할 리스트
profitable_companies = []

# tqdm을 사용하여 진행 상황 표시
for ticker in tqdm(kosdaq_150_tickers, desc="Processing KOSDAQ 150 Tickers"):
    stock = yf.Ticker(ticker)
    
    try:
        # 재무 데이터 (연도별 손익계산서) 가져오기
        income_statement = stock.financials.T
        income_statement = income_statement.reset_index()
        
        # 필요한 열만 선택
        income_statement = income_statement[['index', 'Net Income']]
        
        # 최근 10년간의 데이터만 선택
        recent_years = income_statement.tail(10)
        
        # 순이익 데이터 추출
        net_incomes = recent_years['Net Income'].apply(pd.to_numeric, errors='coerce').fillna(0).values
        dates = recent_years['index'].values
        
        # 2년 이상 연속으로 적자였다가 흑자로 전환 여부 확인
        consecutive_losses = 0
        turned_profitable = False
        turning_point = None
        
        for i in range(len(net_incomes) - 1):
            if net_incomes[i] < 0:
                consecutive_losses += 1
            else:
                consecutive_losses = 0
                
            if consecutive_losses >= 2 and net_incomes[i+1] > 0:
                turned_profitable = True
                turning_point = dates[i+1]
                break

        if turned_profitable:
            profitable_companies.append((ticker, turning_point))
    
    except Exception as e:
        print(f"Error processing {ticker}: {e}")

# 결과 데이터프레임으로 변환
result_df = pd.DataFrame(profitable_companies, columns=['Ticker', 'Turned Profitable Date'])

# 결과 출력
print("2년 이상 연속으로 적자였다가 흑자로 전환한 기업:")
print(result_df)
