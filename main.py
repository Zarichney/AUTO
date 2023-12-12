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
prompt += f"The user has prompted our agency with:\n\n\"{user_message}\"\n\n"
prompt += "Use your tool 'Plan' to generate a plan of action items to accomplish the mission.\n"
prompt += "Please invoke it and return the exact plan generated. We will get the user's acceptance before executing the plan\n"
    
agency.prompt = user_message

response = user_agent.get_completion(message=prompt)

Log(colors.RESULT, f"{user_agent.name}: {response}")

approval_msg = "Waiting for feedback from user. Type 'approve' to execute the plan"

user_message = input(f"{approval_msg}\n\n> ")

while user_message.lower() != "approve":
    response = user_agent.get_completion(message=user_message, useTools=False)
    Log(colors.RESULT, f"{user_agent}: {response}")
    user_message = input(f"{approval_msg}\n\n> ")
    break

prompt = "The user has approved the plan.\n"
prompt += "In order to broadcast the plan to the agency, please respond with the user approved plan and nothing else.\n"

agency.plan = user_agent.get_completion(message=prompt)

# todo
# agency.broadcast(message=the_mission_plan)

# Continue interacting with user agent until the plan is complete
while True:

    # This initiates all agents to co-operate the mission
    response = agency.operate(user_message=prompt)

    # The agency has done their work and require user feedback

    Log(colors.RESULT, f"{agency.active_agent.name}: {response}")

    user_message = input("Waiting for reply from user. Type 'exit' to terminate\n\n> ")

    if user_message.lower() == "exit":
        Log(colors.ACTION, "Exiting...")
        break

    prompt = user_message