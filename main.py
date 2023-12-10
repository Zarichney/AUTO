# /main.py 

import sys
from Agents.Agent import Agent
from Tools.RequestAssistance import RequestAssistance
from Utilities.OpenAiHelper import GetCompletion
from Utilities.Log import Log, colors
from Utilities.Config import GetClient, GetSession

client = GetClient()
agency = GetSession(client)

user_agent:Agent = agency["user"]

# Internal function to call the `RequestAssistance` tool. 
# Supplies the necessary internal components to operate (the agents, threads and client)
def request_assistance(recipient_name,message):
    Log(colors.RED, "recipient_name:", recipient_name, "message:", message)
    result = RequestAssistance(recipient_name=recipient_name,message=message).run(agency, client)
    return result

user_agent.thread = client.beta.threads.create()
user_agent.tools = [request_assistance]

# Program execution

## Sample mission statement:
# Fetch the content of https://en.wikipedia.org/wiki/OpenAI and transpose this wikipedia page to a local markdown file

user_message = sys.argv[1] if len(sys.argv) > 1 else None

while True:
    if user_message is None:
        user_message = input("User: ")

    message = GetCompletion(client, user_message, user_agent)

    Log(colors.GREEN, f"{user_agent.name}: {message}")
    
    user_message = None