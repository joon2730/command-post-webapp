# Command-Post-WebApp
A web-based, visual version of [Command Post CLI](https://github.com/pauljoohyunkim/command-post), built for simplicity and user-friendliness.

## How it Works
**Command Post** is designed as an intelligent assistant that delivers real-time briefings across multiple domains like weather, finance, and news. It combines the power of **LLMs** with a **Retrieval-Augmented Generation (RAG)** architecture to provide up-to-date and context-aware responses.

### Workflow
- Detects request domain (weather, finance, news).
- Fetches live data from APIs.
- Builds context for the LLM.
- Generates response using the LLM.
- Displays output in a web interface.

## How to Run
### Prerequisite
To set up **command-post**, you need [ollama](https://github.com/ollama/ollama) and running.

### Installation
1. Clone the git repository
```shell
git clone {url}
```
2. Install the dependencies.
```shell
pip install -r requirements.txt
```
3. Run app.py to host the app via streamlit
```shell
streamlit run app.py
```

## Usage
Ask about today’s weather, market trends, breaking news, or any real-time updates to get a analytical natural language briefing. (currently supports weather and stock data)
Try ``How is the weather today?``, ``Analyze Bitcoin price trends today``


