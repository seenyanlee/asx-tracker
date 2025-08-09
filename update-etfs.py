import yfinance as yf
import pandas as pd
import json
from datetime import datetime
import os
from pprint import pprint

# ASX ETFs to track
tickers = ["VAE.AX", "ASIA.AX", "IAA.AX", "YMAX.AX", "SYI.AX", "ZYAU.AX", "NDQ.AX", "MVB.AX"]

os.makedirs("docs", exist_ok=True)

def fetch_etf_data():
    etf_data = []
    for ticker in tickers:
        etf = yf.Ticker(ticker)
        info = etf.info
        history = etf.history(period="5y")
        
        # Calculate 3Y/5Y returns (annualized)
        ret_1y = (history["Close"].iloc[-1] / history["Close"].iloc[-252]) - 1 if len(history) > 252 else None  # 252 trading days in a year
        ytd_return = (history["Close"].iloc[-1] / history["Close"].iloc[0]) - 1 if len(history) > 0 else None
        ret_3y = (history["Close"].iloc[-1] / history["Close"].iloc[0]) ** (1/3) - 1 if len(history) > 0 else None
        ret_5y = (history["Close"].iloc[-1] / history["Close"].iloc[0]) ** (1/5) - 1 if len(history) > 0 else None
        
        etf_data.append({
            "Ticker": ticker,
            "Name": info.get("longName", ticker),
            # "Price (AUD)": info.get("currentPrice"),
            "YTD Return (%)": round(ytd_return * 100, 2) if ytd_return else None,
            "1Y Return (%)": round(ret_1y * 100, 2) if ret_1y else None,
            "3Y Return (%)": round(ret_3y * 100, 2) if ret_3y else None,
            "5Y Return (%)": round(ret_5y * 100, 2) if ret_5y else None,
            "P/E Ratio": info.get("trailingPE"),
            "Dividend Yield": info.get("dividendYield") if info.get("dividendYield") else None,
            "Updated": datetime.now().strftime("%Y-%m-%d %H:%M")
        })
    
    # pprint(etf_data)

    # Save data to JSON (for GitHub Pages)
    with open("docs/data.json", "w") as f:
        json.dump(etf_data, f, indent=2)
    
    print("Data updated!")

if __name__ == "__main__":
    fetch_etf_data()