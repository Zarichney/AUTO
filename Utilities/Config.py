# Utilities/Config.py

import json
from openai import OpenAI
from Agents.Agent import Agent
from Tools.ReadFile import ReadFile
from Tools.RequestAssistance import RequestAssistance
from Tools.CreateFile import CreateFile
from Tools.MoveFile import MoveFile
from Tools.ExecutePyFile import ExecutePyFile

gpt3 = "gpt-3.5-turbo"
gpt4 = "gpt-4-1106-preview"
current_model = gpt4


def GetClient():
    openai_key = GetKey()

    client = OpenAI(
        api_key=openai_key,
    )

    return client


def GetKey():
    with open("openai.key", "r") as file:
        return file.read().strip()


def GetSession(client: OpenAI):
    agency = {}

    with open("./session.json", "r") as session_file:
        session = json.load(session_file)
        for agent in session["agents"]:
            agency[agent["key"]] = Agent(agent["key"], agent["id"], client.beta.assistants.retrieve(agent["id"]))

    # Update API with latest from project
    for agent_key in agency:
        agent = agency[agent_key].agent
        agent_tools = []

        if agent_key == "coder":
            agent_tools = (
                [
                    {"type": "function", "function": ReadFile.openai_schema},
                    {"type": "function", "function": MoveFile.openai_schema},
                    {"type": "function", "function": CreateFile.openai_schema},
                    {"type": "function", "function": ExecutePyFile.openai_schema},
                ],
            )
        elif agent_key == "user":
            agent_tools = (
                [
                    {"type": "function", "function": RequestAssistance.openai_schema},
                ],
            )

        # Commented out temporarily: there seems to be an server side API issue
        # Received a 400 BadRequest because the tools type "function" is not being accepted...
        # # Update agent definition
        # agency[agent_key]["agent"] = client.beta.assistants.update(agent.id,
        #     name=agent.name,
        #     description=agent.description if agent.description is not None else "",
        #     instructions=agent.instructions if agent.instructions is not None else "",
        #     model=current_model,
        #     tools=agent_tools,
        # )

    return agency
