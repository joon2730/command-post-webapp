# Command-Post-WebApp
A web-based, visual version of [Command Post CLI](https://github.com/pauljoohyunkim/command-post), built for simplicity and user-friendliness.

## How it Works
**Command Post** is designed as an intelligent assistant that delivers real-time briefings across multiple domains like weather, finance, and news. **Retrieval-Augmented Generation (RAG)** is used to provide up-to-date and context-aware responses.

- New
**Command Post** now deploys multi-agent system with langgraph for more versatile applications. Search agent is bound to tool functions to intellectually select and call apis for real-time data-retrieval. Respond agent generates a final response for user given the real-time data by search agent.

## How to Run
### Prerequisite
To set up **command-post**, you need [ollama](https://github.com/ollama/ollama) and running.
You must use a model supporting tool calling (I personally use llama3.1 and mistral-nemo).

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


