from command_post.ollama_binding import ollama_generate

COMMAND_POST_DOMINS = {
    "weather",
    "news",
    "finance",
    "other"
}

SPINNER_MSG = {
    "weather": "Fetching weather updates...",
    "news": "Fetching latest headlines...",
    "finance": "Fetching financial data...",
}

def determine_domain(prompt : str, config : dict):
    prompt_wrapped = f"Given the following prompt: \"{prompt}\", which domain out of {COMMAND_POST_DOMINS} does it fall into? "
    prompt_wrapped += "Only tell me domain name."
    return ollama_generate(config['command_post_model'], prompt_wrapped).lower().strip()
