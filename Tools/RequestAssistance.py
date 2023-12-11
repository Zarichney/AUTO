# /Tools/RequestAssistance.py

from typing import Dict
from instructor import OpenAISchema
from pydantic import Field
from Agents.Agent import Agent
from Utilities.Helpers import GetAgent
from Utilities.OpenAiHelper import GetCompletion
from Utilities.Log import Log, colors


class RequestAssistance(OpenAISchema):
    """Request assistant from another specialized agent"""

    caller_name: str = Field(
        ..., description="The name of the assistant that invoked this tool"
    )
    recipient_name: str = Field(
        ...,
        description="The agent's name which is being requested for assistance",
    )
    instruction: str = Field(
        ...,
        description="Specify the task required for the recipient agent to complete. Recall the agency's plan and speak to the assistant in terms of the action items you want them to complete.",
    )

    def run(self, agency: Dict[str, Agent], client):
        # find agent by name in agency
        recipient = GetAgent(client, agency, self.recipient_name)
        current_agent = GetAgent(client, agency, self.caller_name)

        # prompt = f"Our agency's mission:\n"
        # prompt += f"{agency['prompt']}\n\n"
        # prompt += f"Our leader has determined the plan:\n"
        # prompt += f"{agency['plan']}\n\n"
        # prompt += f"I, {current_agent.name}, am seeking assistance from you {recipient.name}.\n"
        prompt += "Could you help with the following instructions:\n"
        prompt += self.instruction

        thread = client.beta.threads.create()

        Log(colors.COMMUNICATION, f"Prompting {recipient.name}:", self.instruction)

        response = GetCompletion(
            client=client, message=prompt, agent=recipient, thread=thread
        )

        Log(colors.RESULT, f"{recipient.name} response:", response)

        response += "\n\nWhat is next in the plan?\n"

        return response
