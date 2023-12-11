# /main.py 

import sys
from Agents.Agent import Agent
from Utilities.OpenAiHelper import GetCompletion
from Utilities.Log import Log, colors
from Utilities.Config import GetClient, GetSession

client = GetClient()
agency = GetSession(client)

user_agent:Agent = agency["user"]

# Program execution

user_message = sys.argv[1] if len(sys.argv) > 1 else input("\n\nAUTO: How can I help you?\n\n> ")

Log(colors.ACTION, f"\nThinking...\n")
        
prompt = f"{user_agent.name}, I request your help\n"
prompt += f"The user has prompted you for \"{user_message}\"\n"
prompt += "You are to use your tool 'MakePlan' to generate a plan of action items to accomplish the mission.\n"
prompt += "Please invoke it and return the exact plan generated from the tool before we begin executing the plan.\n"
    
the_mission_plan = GetCompletion(client, prompt, user_agent)

# agency['plan'] = the_mission_plan
# agency['prompt'] = user_message

Log(colors.RESULT, f"{user_agent.name}: {the_mission_plan}")

prompt = "Execute the plan accordingly.\n"
prompt += "Use your tool 'RequestAssisance' on the first agent in the plan,"
prompt += " providing them with the plan and their instructions\n"

prompt += f"\n\nTHE PLAN:\n{the_mission_plan}"

Log(colors.ACTION, f"\nExecuting Plan...\n\n")

while True:

    results = GetCompletion(client, prompt, user_agent)

    Log(colors.RESULT, f"{user_agent.name}: {results}")
    
    user_message = input("Waiting for reply from user\n\n> ")
    
    prompt = user_message