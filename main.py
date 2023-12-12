# /main.py 

import sys
from Agents.Agent import Agent
from Agents.Agency import Agency
from Agents import UserAgent
from Utilities.Log import Log, colors

agency:Agency = Agency(new_session=True)

user_agent:Agent = agency.get_agent(UserAgent.name)

user_message = sys.argv[1] if len(sys.argv) > 1 else input("\n\nAUTO: How can I help you?\n\n> ")

# todo store the prompt to file and if the user provides the same prompt
# inquire with user whether we should continue session or restart

Log(colors.ACTION, f"\nThinking...\n")
        
prompt = f"{user_agent.name}, I request your help\n"
prompt += f"The user has prompted you for \"{user_message}\"\n"
prompt += "You are to use your tool 'Plan' to generate a plan of action items to accomplish the mission.\n"
prompt += "Please invoke it and return the exact plan generated from the tool before we begin executing the plan.\n"
    
the_mission_plan = user_agnet.get_completion(message=prompt)

# todo:
# agency['plan'] = the_mission_plan
# agency['prompt'] = user_message

Log(colors.RESULT, f"{user_agent.name}: {the_mission_plan}")

prompt = "Execute the plan accordingly.\n"
prompt += "Use your tool 'RequestAssisance' on the first agent in the plan,"
prompt += " providing them with the plan and their instructions\n"

prompt += f"\n\nTHE PLAN:\n{the_mission_plan}"

Log(colors.ACTION, f"\nExecuting Plan...\n\n")

# Continue interacting with user agent until the plan is complete
while True:
    results = user_agent.get_completion(message=prompt)

    Log(colors.RESULT, f"{user_agent.name}: {results}")

    user_message = input("Waiting for reply from user. Type 'exit' to terminate\n\n> ")

    if user_message.lower() == "exit":
        Log(colors.ACTION, "Exiting...")
        break

    prompt = user_message