from command_post.modules.finance import download_stock_data
from typing import Callable
from langchain_core.tools import tool
import requests
import json
# from datetime import datetime

# Special tool functions
@tool
def data_not_required():
    """
    Called when no data is required to answer user's message
    """
    return """\
No real-time data required to answer to user's message.
Answer freely with your commmon knowledage base.
If user message is conversational, answer in conversational tone.
Keep in mind that user is your commander, be formal and concise, but don't make any stories up.
"""

@tool
def data_not_available():
    """
    Called when there is no appropriate tool function to get desired data
    """
    return "No tools available to get necessary data.\nExplain user that you have no access to data in requested domain."

TOOLS = [
    # Tools
    download_stock_data,

    # Special Tools
    data_not_required,
    data_not_available,
]

# Register all tool functions here
AVAILABLE_TOOLS: dict[str, Callable] = {tool.name: tool for tool in TOOLS}

def get_location(get_raw=False):
    IP_API = "http://ip-api.com/json/"
    r = requests.get(IP_API)
    data = json.loads(r.content.decode())
    if get_raw:
        return data
    else:
        return {
            "lat": data["lat"],
            "lon": data["lon"],
            "country": data["country"],
            "timezone": data["timezone"]
        }