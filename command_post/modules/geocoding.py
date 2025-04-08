import requests
import json

def get_coords(search_term):
    r = requests.get(f"https://geocoding-api.open-meteo.com/v1/search?name={search_term}&count=1&language=en&format=json")
    data = json.loads(r.content)
    return (data["results"][0]["latitude"], data["results"][0]["longitude"])