# /agent_setup.py

# This purpose of this file is to have the definitions from /Agents/<agent_name>.py created in the OpenAI API.
# After client.beta.assistants.create is called, the assistant object is returned which the id field needs to be stored in
# ./session.json as {"assistants":[{"id": <assistant.id>, "key": <hardcoded> }, ...]}
    
import json
from openai import OpenAI
from Agents import UserProxyAgent, CodingAgent 
from Tools.ReadFile import ReadFile
from Tools.RequestAssistance import RequestAssistance
from Tools.CreateFile import CreateFile
from Tools.MoveFile import MoveFile
from Tools.ExecutePyFile import ExecutePyFile
from Utilities.Connection import GetKey

gpt3 = "gpt-3.5-turbo"
gpt4 = "gpt-4-1106-preview"
current_model = gpt4
openai_key = GetKey()

client = OpenAI(
    api_key=openai_key,
)
    
# Coder agent setup
code_assistant = client.beta.assistants.create(
    name=CodingAgent.name,
    instructions=CodingAgent.instructions,
    model=current_model,
    tools=[
        {"type": "function", "function": ReadFile.openai_schema},
        {"type": "function", "function": MoveFile.openai_schema},
        {"type": "function", "function": CreateFile.openai_schema},
        {"type": "function", "function": ExecutePyFile.openai_schema},
    ],
)

# User agent setup
user_proxy = client.beta.assistants.create(
    name=UserProxyAgent.name,
    instructions=UserProxyAgent.instructions,
    model=current_model,
    tools=[
        {"type": "function", "function": RequestAssistance.openai_schema},
    ],
)

# Log the assistant ids to ./session.json
with open("./session.json", "w") as session_file:
    assistants = [
        {"id": code_assistant.id, "key": "coder"},
        {"id": user_proxy.id, "key": "user"}
    ]
    json.dump({"assistants": assistants}, session_file)

