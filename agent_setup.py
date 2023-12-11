# /agent_setup.py

# This purpose of this file is to have the definitions from /Agents/<agent_name>.py created in the OpenAI API.
# After client.beta.assistants.create is called, the assistant object is returned which the id field needs to be stored in
# ./session.json as {"assistants":[{"id": <assistant.id>, "key": <hardcoded> }, ...]}

import json
from openai import OpenAI
from Agents import UserAgent, CodingAgent, QaAgent, RecipeAgent
from Tools.ReadFile import ReadFile
from Tools.MakePlan import MakePlan
from Tools.RequestAssistance import RequestAssistance
from Tools.CreateFile import CreateFile
from Tools.MoveFile import MoveFile
from Tools.ExecutePyFile import ExecutePyFile
from Utilities.Config import GetClient, current_model

client = GetClient()

# User agent setup
user_agent = client.beta.assistants.create(
    name=UserAgent.name,
    description=UserAgent.description,
    instructions=UserAgent.instructions,
    model=current_model,
    metadata={"key": "user", "services": UserAgent.services},
    tools=[
        {"type": "function", "function": MakePlan.openai_schema},
        {"type": "function", "function": ReadFile.openai_schema},
        {"type": "function", "function": MoveFile.openai_schema},
        {"type": "function", "function": RequestAssistance.openai_schema},
    ],
)

# Coder agent setup
coder_agent = client.beta.assistants.create(
    name=CodingAgent.name,
    description=CodingAgent.description,
    instructions=CodingAgent.instructions,
    model=current_model,
    metadata={"key": "coder", "services": CodingAgent.services},
    tools=[
        {"type": "function", "function": MakePlan.openai_schema},
        {"type": "function", "function": RequestAssistance.openai_schema},
        {"type": "function", "function": ReadFile.openai_schema},
        {"type": "function", "function": MoveFile.openai_schema},
        {"type": "function", "function": CreateFile.openai_schema},
        {"type": "function", "function": ExecutePyFile.openai_schema},
    ],
)

# QA agent setup
qa_agent = client.beta.assistants.create(
    name=QaAgent.name,
    description=QaAgent.description,
    instructions=QaAgent.instructions,
    model=current_model,
    metadata={"key": "qa", "services": QaAgent.services},
    tools=[
        {"type": "function", "function": MakePlan.openai_schema},
        {"type": "function", "function": RequestAssistance.openai_schema},
        {"type": "function", "function": ReadFile.openai_schema},
        {"type": "function", "function": MoveFile.openai_schema},
        {"type": "function", "function": CreateFile.openai_schema},
        {"type": "function", "function": ExecutePyFile.openai_schema},
    ],
)

# Log the assistant ids to ./session.json
with open("./session.json", "w") as session_file:
    assistants = [
        {"id": coder_agent.id, "key": "coder"},
        {"id": user_agent.id, "key": "user"},
        {"id": qa_agent.id, "key": "qa"},
    ]
    json.dump({"agents": assistants}, session_file)
