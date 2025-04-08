from command_post.modules import weather, finance

def generate_context_prompt(query, domain, config):
    """
    Generate a context prompt for the given query and domain.
    """
    if domain == "weather":
        return weather.generate_weather_report(query, config)
    elif domain == "news":
        return f"Given the following query: \"{query}\", generate a news summary."
    elif domain == "finance":
        return finance.generate_finance_report(query, config)
    else:
        return f"Given the following query: \"{query}\", generate a general response."