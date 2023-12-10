# /main.py 

import sys
from Tools.RequestAssistance import RequestAssistance
from Utilities.OpenAiHelper import GetCompletion
from Utilities.Log import Log, colors
from Utilities.Config import GetClient, GetSession

client = GetClient()
agency = GetSession(client)

coder_agent = agency["coder"].agent
user_agent = agency["user"].agent

thread = client.beta.threads.create()

# Internal function to call the `RequestAssistance` tool. 
# Supplies the necessary internal components to operate (the agents, threads and client)
def request_assistance(recipient,message):
    result = RequestAssistance(recipient=recipient,message=message).run(agency, client)
    return result

# Program execution

## Sample mission statement:
# Fetch the content of https://en.wikipedia.org/wiki/OpenAI and transpose this wikipedia page to a local markdown file

user_message = sys.argv[1] if len(sys.argv) > 1 else None

while True:
    if user_message is None:
        user_message = input("User: ")

    message = GetCompletion(client, user_message, user_agent, [request_assistance], thread)

    Log(colors.GREEN, f"{user_agent.name}: {message}")
    
    user_message = None