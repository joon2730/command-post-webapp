import json
import os
import datetime
import hashlib
import string
from datetime import datetime, timezone
from command_post.ollama_binding import ollama_create_model, ollama_pull

def init_config() -> dict:
    home = os.path.expanduser("~")
    config_dirpath = os.path.join(home, ".cpconfig")
    config_filepath = os.path.join(config_dirpath, "config.json")
    modelfile_filepath = os.path.join(config_dirpath, "Modelfile")

    if os.path.isdir(config_dirpath):
        confirmation = input(f"{config_dirpath} already exists. If you want this directory to be overwritten, type \"overwrite\" exactly (without the quotation marks): ")
        if confirmation != "overwrite":
            raise Exception(f"User decided not to overwrite directory {config_dirpath}")
    else:
        os.mkdir(config_dirpath)
        print(f"Configuration created at {config_dirpath}")
    
    if os.path.isfile(config_filepath):
        print(f"Configuration file {config_filepath} already exists. Doing nothing.")
    
    # Writing initial configuration.
    config = {
        "base_model": "",
        "assistant_name": "",
        "temperature": 0.0,
        "command_post_model": "",
        "modified_model_sha256": "",
        "model_creation": ""
    }

    # TODO: *Asynchronously* pull ollama model
    ollama_model = input("Ollama model: ").strip()
    ollama_pull(ollama_model)
    assistant_name = "Eve"
    temperature = 0.2
    config["base_model"] = ollama_model
    config["command_post_model"] = f"{ollama_model}_cp"
    config["assistant_name"] = assistant_name
    config["temperature"] = temperature

#    system_prompt = """
#Your name is $assistant_name.
#When asked what you are, you must say that you are a CP, a command post,
#and you are supposed to introduce yourself.
#Do not ask any question back at the end.
#Your job is to give a summary on data that is given.
#Start your answer immediately. 
#    """
    system_prompt = """
Your name is $assistant_name.
You are a command post.
Do not introduce yourself when answering.
Do not ask any question back at the end.
Your job is to give a summary on data that is given.
Start your answer immediately. 
    """
    system_prompt = string.Template(system_prompt).safe_substitute(assistant_name=assistant_name)

    # Build Modelfile
    # Choose what model to base off.
    modelfile_template = """
FROM $ollama_model

# Creativity.
PARAMETER temperature $temp

SYSTEM \"\"\"
$system_prompt
\"\"\"
"""
    modelfile = string.Template(modelfile_template).safe_substitute(ollama_model=ollama_model,temp=temperature, system_prompt=system_prompt)
    with open(modelfile_filepath, "w") as file:
        file.write(modelfile)

    # Compute hash of the modelfile.
    s = hashlib.sha256()
    s.update(modelfile.encode())
    config["modified_model_sha256"] = s.hexdigest()

    # Create model
    # TODO: Call Ollama API to create model
    ollama_create_model(config["command_post_model"], ollama_model, system_prompt, temperature)
    print("Created model " + config["command_post_model"])
    config["model_creation"] = datetime.now(timezone.utc).isoformat()

    # Write config file
    with open(config_filepath, "w") as file:
        json.dump(config, file)

    return config

def read_config() -> dict:
    home = os.path.expanduser("~")
    config_dirpath = os.path.join(home, ".cpconfig")
    config_filepath = os.path.join(config_dirpath, "config.json")
    modelfile_filepath = os.path.join(config_dirpath, "Modelfile")

    if os.path.isdir(config_dirpath):
        # Read the config json file
        with open(config_filepath, "r") as file:
            config = json.load(file)
        
        # Compute the hash of the modelfile and see if the model needs to be recreated.
        with open(modelfile_filepath, "rb") as file:
            s = hashlib.sha256()
            s.update(file.read())
            if config["modified_model_sha256"] != s.hexdigest():
                # TODO: Read Modelfile and change.
                print("Modelfile change detected!")
                pass
    else:
        raise FileNotFoundError(f"Configuration directory {config_dirpath} not found.")
    
    return config

class Config():
    def __init__(self):
        self.config = read_config()
        self.base_model = self.config["base_model"]
        self.assistant_name = self.config["assistant_name"]
        self.temperature = self.config["temperature"]
        self.command_post_model = self.config["command_post_model"]
        self.modified_model_sha256 = self.config["modified_model_sha256"]
        self.model_creation = datetime.fromisoformat(self.config["model_creation"])