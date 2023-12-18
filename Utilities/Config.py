# Utilities/Config.py

from openai import OpenAI

gpt3 = "gpt-3.5-turbo-1106"
gpt4 = "gpt-4-1106-preview"
current_model = gpt3

session_file_name = "./sessions.json"
agent_config_file_name = "./agents.json"

def GetClient():
    openai_key = GetKey()

    client = OpenAI(
        api_key=openai_key,
    )

    return client

def GetKey():
    with open("openai.key", "r") as file:
        return file.read().strip()
