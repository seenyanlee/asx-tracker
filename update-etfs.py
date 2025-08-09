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
        # ret_1y = (history["Close"].iloc[-1] / history["Close"].iloc[-252]) - 1 if len(history) > 252 else None  # 252 trading days in a year
        ret_3y = info.get("threeYearAverageReturn", None)
        ret_5y = info.get("fiveYearAverageReturn", None)

        etf_data.append({
            "Ticker": ticker,
            "Name": info.get("longName", ticker),
            "Price (AUD)": info.get("previousClose"),
            "Average 10-day Volume": info.get("averageVolume10days"),
            "YTD Return (%)": info.get("ytdReturn", None),
            # "1Y Return (%)": round(ret_1y * 100, 2) if ret_1y else None,
            "3Y Return (%)": round(ret_3y * 100, 2) if ret_3y else None,
            "5Y Return (%)": round(ret_5y * 100, 2) if ret_5y else None,
            "P/E Ratio": info.get("trailingPE"),
            "Dividend Yield": info.get("dividendYield", None),
            "52 Week High": info.get("fiftyTwoWeekHigh"),
            "52 Week Low": info.get("fiftyTwoWeekLow"),
            "Inception Date": pd.to_datetime(info.get("fundInceptionDate"), unit='s').strftime('%Y-%m-%d') if info.get("fundInceptionDate") else None,
            "Updated": datetime.now().strftime("%Y-%m-%d %H:%M")
        })
    
    # pprint(etf_data)

    # Save data to JSON (for GitHub Pages)
    with open("docs/data.json", "w") as f:
        json.dump(etf_data, f, indent=2)
    
    print("Data updated!")

if __name__ == "__main__":
    fetch_etf_data()