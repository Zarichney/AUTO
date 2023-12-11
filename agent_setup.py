# /agent_setup.py

# This purpose of this file is to have the definitions from /Agents/<agent_name>.py created in the OpenAI API.
# After client.beta.assistants.create is called, the assistant object is returned which the id field needs to be stored in
# ./session.json as {"assistants":[{"id": <assistant.id>, "key": <hardcoded> }, ...]}

import json
from Agents import TeamMember, UserAgent, CodingAgent, QaAgent, RecipeAgent
from Tools.ReadFile import ReadFile
from Tools.MakePlan import MakePlan
from Tools.RequestAssistance import RequestAssistance
from Tools.CreateFile import CreateFile
from Tools.MoveFile import MoveFile
from Tools.ExecutePyFile import ExecutePyFile
from Utilities.Config import GetClient, current_model
import json
import json

client = GetClient()

# Build a generic team member instruction set that will be prepended to each agent's instructions

# Make them aware of the agents available:
team_member_instructions = TeamMember.team_instruction
team_member_instructions += "\n## Agency\n"
for agent in [UserAgent, CodingAgent, QaAgent, RecipeAgent]:
    team_member_instructions += "### " + agent.name + "\n" 
    team_member_instructions += agent.description + "\n"
    team_member_instructions += agent.services + "\n"
team_member_instructions += "\n\n"

# Make them aware of the tools available:
team_member_instructions += TeamMember.tool_instruction
team_member_instructions += "\n## Tools\n"
for toolFile in [ReadFile, CreateFile, MoveFile, ExecutePyFile, RequestAssistance, MakePlan]:
    schema = toolFile.openai_schema
    team_member_instructions += "### " + schema['name'] + "\n"
    team_member_instructions += schema['description'] + "\n\n"
team_member_instructions += "\n\n"

# User agent setup
user_agent = client.beta.assistants.create(
    name=UserAgent.name,
    description=UserAgent.description,
    instructions=UserAgent.instructions + team_member_instructions,
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
    instructions=CodingAgent.instructions + team_member_instructions,
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
    instructions=QaAgent.instructions + team_member_instructions,
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

recipe_agent = client.beta.assistants.create(
    name=RecipeAgent.name,
    description=RecipeAgent.description,
    instructions=RecipeAgent.instructions + team_member_instructions,
    model=current_model,
    metadata={"key": "recipe", "services": RecipeAgent.services},
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
