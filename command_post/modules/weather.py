import yfinance as yf
import json
from langchain_core.tools import tool
import pandas as pd
from typing import Annotated
import requests

def get_weather(location, start_date, end_date):
    if type(location) == tuple:
        lat, lon = location
    else:
        if location:
            lat, lon = get_coords(location)
        else:
            lat, lon = get_location()
    OPEN_METEO = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m,rain,relative_humidity_2m,uv_index&start_date={start_date}&end_date={end_date}&timezone=auto"
    r = requests.get(OPEN_METEO)
    raw_data = json.loads(r.content.decode())

    processed_data = {
        "temperature (C)": {i:j for i, j in zip(raw_data["hourly"]["time"], raw_data["hourly"]["temperature_2m"])},
        "rain (mm)": {i:j for i, j in zip(raw_data["hourly"]["time"], raw_data["hourly"]["rain"])},
        #"relative humidity (%)": {i:j for i, j in zip(raw_data["hourly"]["time"], raw_data["hourly"]["relative_humidity_2m"])},
        #"UV index": {i:j for i, j in zip(raw_data["hourly"]["time"], raw_data["hourly"]["uv_index"])}
    }
    return processed_data

def generate_weather_report(prompt, config, verbose=False, length="a paragraph", visual=True):
    if verbose:
        print("Filtering weather parameters.")
    weather_params = filter_weather_params(prompt, config)
    start_date = weather_params[0]
    end_date = weather_params[1]
    location = weather_params[2]

    if verbose:
        print(f"Getting weather data for {location} from {start_date} to {end_date}")
    data = get_weather(location, start_date, end_date)

    wrapped_prompt = f"It is currently {datetime.datetime.now().isoformat()}. "
    wrapped_prompt += "Given the following weather data \n"
    wrapped_prompt += json.dumps(data) + '\n'
    wrapped_prompt += f"Give an analyzed response to \"{prompt}\" "
    wrapped_prompt += f"in {length}" if length else ""
    
    return wrapped_prompt, data["temperature (C)"]