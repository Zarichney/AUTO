# /main.py 

import sys
from Agents.Agent import Agent
from Agents.Agency import Agency
from Agents import UserAgent
from Utilities.Log import Log, Debug, colors

user_message = sys.argv[1] if len(sys.argv) > 1 else input("\n\nAUTO: How can I help you?\n\n> ")

agency:Agency = Agency(prompt=user_message, new_session=False, build_agents=False)

user_agent:Agent = agency.get_agent(UserAgent.name)
agency.active_agent = user_agent

# todo inquire with user whether we should continue session or restart

Log(colors.ACTION, f"Processing...")
        
prompt = f"{user_agent.name}, I request your help\n"
prompt += f"The user has prompted our agency with:\n\n\"{user_message}\"\n\n"
prompt += "Use your tool 'Plan' to generate a plan of action items to accomplish the mission.\n"
prompt += "Please invoke it and return the exact plan generated. Do not change the output of the 'Plan' tool.\n"
prompt += "We will get the user's acceptance before executing the plan\n"
    
agency.prompt = user_message

# todo, fix this: this cant be the plan as it rarely adheres to the tool output <- this is what we want to capture, store and broadcast
response = user_agent.get_completion(message=prompt)

approval_msg = "Waiting for feedback from user. Type 'approve' to execute the plan"

user_message = input(f"{approval_msg}\n\n> ")

while user_message.lower() != "approve":
    response = user_agent.get_completion(message=user_message, useTools=False)
    Log(colors.RESULT, f"{user_agent.name}: {response}")
    user_message = input(f"{approval_msg}\n\n> ")
    break

agency.plan = response
Debug(f"Saving response as agency plan: {agency.plan}")

prompt = "The user has approved the plan.\n"
prompt += "Execute the plan accordingly.\n"
prompt += "If you are not the agent in step 1, then use your tool 'Delegate' on the first agent in the plan.\n"
prompt += "Providing them with their mission\n"

Log(colors.ACTION, f"Executing Plan...")

# Continue interacting with user agent until the plan is complete
while True:

    # This initiates all agents to co-operate the mission
    try:
        response = agency.operate(prompt=prompt)
    except Exception as e:
        Log(colors.ERROR, f"Error in main.py: {e}")

    # The agency has done their work and require user feedback

    Log(colors.RESULT, f"{agency.active_agent.name}:\n{response}")

    prompt = input("Waiting for reply from user. Type 'exit' to terminate\n\n> ")

    if prompt.lower() == "exit":
        Log(colors.ACTION, "Exiting...")
        break

    Log(colors.ACTION, f"Processing...")
