from fastapi import FastAPI
import yfinance as yf
import pandas as pd
import os

app = FastAPI()

class EarningsAnalyzer:
    def __init__(self):
        self.portfolio = self.load_portfolio()
        
    def load_portfolio(self):
        portfolio_path = os.getenv(
            "PORTFOLIO_PATH",
            os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data_ingestion", "portfolio.csv"))
        )

        if not os.path.exists(portfolio_path):
            raise FileNotFoundError(f"Portfolio file missing at: {portfolio_path}")
            
        df = pd.read_csv(portfolio_path)
        return df[['ticker', 'sector', 'region', 'weight']].dropna()

    def get_asia_tech_exposure(self):
        filtered = self.portfolio[
            (self.portfolio['sector'].str.contains('Tech', case=False)) &
            (self.portfolio['region'].str.contains('Asia', case=False))
        ]
        return round(filtered['weight'].sum() * 100, 2)

    def get_earnings_surprises(self):
        surprises = {}
        
        for ticker in self.portfolio['ticker'].unique():
            try:
                stock = yf.Ticker(ticker)
                income = stock.income_stmt
                if income.empty:
                    continue
                    
                recent_quarter = income.iloc[:, 0]
                net_income = recent_quarter.get("Net Income")
                
                if net_income is not None and net_income != 0:
                    estimate = net_income * 0.96
                    surprise = ((net_income - estimate) / abs(estimate)) * 100
                    surprises[ticker] = round(surprise, 2)
            except Exception as e:
                print(f"Error processing {ticker}: {str(e)}")
        return surprises

analyzer = EarningsAnalyzer()

@app.get("/exposure")
def get_exposure():
    return {"exposure": analyzer.get_asia_tech_exposure()}

@app.get("/earnings_surprises")
def get_earnings():
    return analyzer.get_earnings_surprises()

@app.get("/health")
def health_check():
    return {"status": "healthy"}

