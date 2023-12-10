# /main.py 

import json
from openai import OpenAI
from Agents import UserProxyAgent, CodingAgent 
from Tools.ReadFile import ReadFile
from Tools.RequestAssistance import RequestAssistance
from Tools.CreateFile import CreateFile
from Tools.MoveFile import MoveFile
from Tools.ExecutePyFile import ExecutePyFile
from Utilities.Connection import GetKey
from Utilities.OpenAiHelper import GetCompletion
from Utilities.Log import Log, colors

# Config stuff
openai_key = GetKey()

client = OpenAI(
    api_key=openai_key,
)

## Simple completion test:
# completion = client.chat.completions.create(
#   model=gpt3,
#   messages=[
#     {"role": "system", "content": system_message},
#     {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming"}
#   ]
# )
# print(completion.choices[0].message)

## Sample mission statement:
# Fetch the content of https://en.wikipedia.org/wiki/OpenAI and transpose this wikipedia page to a local markdown file

# Get session info from ./session.json
# ./session.json as {"assistants":[{"id": <assistant.id>, "key": <assistant.key>}, ...]}
with open("./session.json", "r") as session_file:
    session = json.load(session_file)
    # Iterate over the assistans and store the id and name in a dictionary
    assistants = {}
    for assistant in session["assistants"]:
        assistants[assistant["key"]] = assistant["id"]

coder_agent = client.beta.assistants.retrieve(assistants["coder"])
user_agent = client.beta.assistants.retrieve(assistants["user"])

thread = client.beta.threads.create()

# This is used to tie agents and their tools
agents_and_threads = {
    "user": {
        "agent": user_agent,
        "thread": None,
        "funcs": [RequestAssistance]
    },
    "coder": {
        "agent": coder_agent,
        "thread": None,
        "funcs": [ReadFile, MoveFile, CreateFile, ExecutePyFile]
    }
}

# Internal function to call the `RequestAssistance` tool. 
# Supplies the necessary internal components to operate (the agents, threads and client)
def request_assistance(recipient,message):
    result = RequestAssistance(recipient=recipient,message=message).run(agents_and_threads, client)
    return result

# Program execution
while True:
    user_message = input("User: ")

    message = GetCompletion(client, user_message, user_agent, [request_assistance], thread)

    Log(colors.GREEN, f"{user_agent.name}: {message}")
