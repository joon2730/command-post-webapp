ollama_models = {
    # "openchat7b": "openchat:7b-v3.5-0106",
    # "nemotron": "nemotron-mini:latest",
    # "deepseek8b": "deepseek-r1:8b",
    # "gemma12b": "gemma3:12b",
    "llama8b": "llama3.1:latest",
    "mistral-nemo": "mistral-nemo:latest",
}

class Config:
    ollama_model_name = ollama_models["mistral-nemo"]
    model_temperature = 0.4
    model_max_tokens = 1000
    language = "English"