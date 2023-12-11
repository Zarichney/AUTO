# /Utilities/Helpers.py

from typing import Dict

from Agents.Agent import Agent
from Utilities.Log import Log, colors


def GetAgent(client, agency: Dict[str, Agent], agentName):
    agent = next((agent for agent in agency.values() if agent.name == agentName), None)

    if agent:
        return agent

    # An invalid name was supplied, use GPT to find the correct agent name

    message = (
        "List of agents: "
        + ", ".join([agent.name for agent in agency.values()])
        + "\n\nWhat is the actual agent name for: "
        + agentName
        + "\nTell me the agent name and nothing else."
    )
    
    Log(colors.ERROR, f"Agent {agentName} not found in agency. Engaging fall back:\n\n{message}")

    completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {
                "role": "system",
                "content": "Solve this small problem. The prompt will be provide you a list of agent names and a mismatched name. The goal is to select the closest resembling agent name based off the one provide.You must answer with only the correct agent name and nothing else.",
            },
            {
                "role": "user",
                "content": message,
            },
        ],
    )
    response = completion.choices[0].message.content
    
    actualAgentName = response

    Log(colors.ERROR, f"Agent name fallback determined: {actualAgentName}")

    agent = next(
        (agent for agent in agency.values() if agent.name == actualAgentName), None
    )

    if not agent:
        Log(colors.ERROR, f"Agent {agentName} not found in agency.")
        return

    return agent
