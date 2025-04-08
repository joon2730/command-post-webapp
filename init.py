import requests
import sys
import os
from command_post.config import init_config

if __name__ == "__main__":
    init_config()
    print("command_post initialized! Start by running \"streamlit run app.py\"")
    sys.exit(0)
