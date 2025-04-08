import yfinance as yf
import json
from datetime import datetime
from zoneinfo import ZoneInfo
from command_post.ollama_binding import ollama_generate

def generate_finance_report(prompt, config, period="3d", interval="1h", timezone="America/New_York", length="a paragraph", verbose=True, visual=True):

    # Determine the ticker symbol from the prompt
    prompt = f"Given the following prompt: \"{prompt}\", if this is a name of a security in the stock market, give its yfinance ticker symbol. If not, output \"None\".\n"
    prompt += "Only print either the symbol or None"
    
    ticker = ollama_generate(config["command_post_model"], prompt).strip()

    print(f"Ticker: {ticker}")
    
    if ticker == "None":
        raise Exception(f"No ticker symbol found in the prompt {prompt}.")

    # Download the data using yfinance
    try:
        df = yf.download(ticker, period=period, interval=interval, auto_adjust=True)
        df.index = df.index.tz_convert(timezone)
        df.index = df.index.strftime("%Y-%m-%d %H:%M")
        data = df["Close"][ticker].to_dict()
        assert data, "Data is empty"
    except Exception as e:
        raise Exception(f"Failed to download data for ticker {ticker}: {e}")
    
    # Write the prompt for the model
    wrapped_prompt = f"It is currently {datetime.now().astimezone(ZoneInfo(timezone)).isoformat()} in timezone {timezone}. "
    wrapped_prompt += f"You have acquired a close price data for {ticker} over the period {period}, in timezone {timezone}, \n"
    wrapped_prompt += json.dumps(data) + "\n"
    wrapped_prompt += f"Now give an analyzed response to {ticker} focused on the highs, lows, percentage change, and trends"
    wrapped_prompt += f"in {length}" if length else ""
    wrapped_prompt += "Mention the start and end datetime of the data with the timezone for clarity, and round the values to 2 decimal places."
    wrapped_prompt += "Note that the response is to be read by tts, so avoid using any special characters or formatting, and replace any symbols and acronyms (e.g. tickers) to natural language."

    return wrapped_prompt, df["Close"][ticker]