import ollama

def ollama_create_model(dest_model_name, src_model_name, system, temperature=0.2):
    ollama.create(model=dest_model_name, from_=src_model_name, system=system, parameters={"temperature": temperature})

def ollama_chat_request(model_name, prompt):
    response = ollama.chat(model=model_name, messages=[
    {
        'role': 'user',
        'content': prompt,
    }
    ], stream=False)
    return response['message']['content']

def ollama_generate(model_name, prompt):
    response = ollama.generate(model=model_name, prompt=prompt)
    return response['response']

def ollama_pull(model_name):
    ollama.pull(model_name)