# /Tools/Delegate.py

from instructor import OpenAISchema
from pydantic import Field
from Agents.Agent import Agent
from Agents.Agency import Agency
from Utilities.Helpers import GetCompletion
from Utilities.Log import Log, colors

class Delegate(OpenAISchema):
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

    def run(self, agency: Agency):
        # find agent by name in agency
        recipient: Agent = agency.get_agent(self.recipient_name)
        current_agent: Agent = agency.get_agent(self.caller_name)

        # prompt = f"Our agency's mission:\n"
        # prompt += f"{agency['prompt']}\n\n"
        # prompt += f"Our leader has determined the plan:\n"
        # prompt += f"{agency['plan']}\n\n"
        # prompt += f"I, {current_agent.name}, am seeking assistance from you {recipient.name}.\n"
        prompt = "Could you help with the following instructions:\n"
        prompt += self.instruction

        Log(colors.COMMUNICATION, f"Prompting {recipient.name}:", self.instruction)

        # todo make this async so that the current agent can close the run while the recipient agent starts a new run
        response = GetCompletion(agency=agency, agent=recipient, message=prompt)

        Log(colors.RESULT, f"{recipient.name} response:", response)

        response += "\n\nWhat is next in the plan?\n"

        return response
