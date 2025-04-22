import yfinance as yf
import json
# from datetime import datetime
# from zoneinfo import ZoneInfo
from langchain_core.tools import tool
import pandas as pd
from typing import Annotated

@tool
def download_stock_data(
    ticker: Annotated[str, "The stock symbol in Yfinance"], 
    period: Annotated[str, "Time range to fetch data ('1d', '5d', '1mo', '3mo', '6mo', '1y')"], 
    interval: Annotated[str, "Data granularity ('1m', '5m', '1h', '1d', '1wk', '1mo')"]
):
    """
    Get real-time close price of stock, crypto, ETF, etc.
    """
    df = yf.download(ticker, period=period, interval=interval, progress=False)
    if df.empty:
        return json.dumps({"error": f"No data found for {ticker}."})
    
    # Format datetime index and round numeric values
    df.index = pd.to_datetime(df.index)
    df.index = df.index.strftime("%Y-%m-%d %H:%M")
    df = df.round(2)

    # Create close_price list as list of [date, close] pairs
    close_price = [
        [date, float(close)] for date, close in zip(df.index, df["Close"][ticker])
    ]

    result = {
        "ticker": ticker,
        "period": period,
        "interval": interval,
        "close_price": close_price
    }

    return json.dumps(result, ensure_ascii=False, indent=2)
    # return {
    #     "description": f"Close price of {ticker} for recent {period} with {interval} interval.", 
    #     "dataframe": df["Close"][ticker],
    #     "json": json.dumps(result, ensure_ascii=False, indent=2)
    # }

