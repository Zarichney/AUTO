# /main.py

import sys
from Agents import BaseAgent, UserAgent
from Agents.BaseAgent import BaseAgent
from Agency.Agency import Agency
from Utilities.Log import Log, Debug, type

user_message = (
    sys.argv[1] if len(sys.argv) > 1 else input("\n\nAUTO Agency: What is your mission?\n\n> ")
)

agency: Agency = Agency(prompt=user_message, new_session=False, rebuild_agents=False)

user_agent: BaseAgent = agency.get_agent(UserAgent.NAME)
agency.active_agent = user_agent

Log(type.ACTION, f"Processing...")

prompt = f"Agency, you are being engaged to fulfill the user's mission\n"
prompt += f'The user has prompted our agency with:\n\n"{user_message}"\n\n'

prompt += "Use your tool 'Plan' to review the agency's team and arsenal and generate a workflow of action items to accomplish the mission.\n"
prompt += "Respond with the plan for the user to review. We will wait for the user's acceptance prior to executing the plan.\n"

agency.plan = agency.complete(
    mission_prompt=prompt,
    single_agent=True,
    stop_word="approve",
    continue_phrase="Execute the plan",
)
Debug(f"Saving response as agency plan: {agency.plan}")

prompt = "The user has approved the plan.\n"
prompt += "Execute the plan accordingly.\n"
prompt += "If you are not the agent in step 1, then use your tool 'Delegate' on the first agent in the plan.\n"
prompt += "Providing them with their mission\n"

Log(type.ACTION, f"Executing Plan...")

agency.complete(
    mission_prompt=prompt,
    single_agent=False,
    stop_word="exit",
    continue_phrase="terminate",
)
