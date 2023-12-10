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
from Utilities.Config import GetClient, current_model

client = GetClient()
    
# Coder agent setup
coder_agent = client.beta.assistants.create(
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
user_agent = client.beta.assistants.create(
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
        {"id": coder_agent.id, "key": "coder"},
        {"id": user_agent.id, "key": "user"}
    ]
    json.dump({"agents": assistants}, session_file)

