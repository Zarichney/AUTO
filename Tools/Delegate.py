# /Tools/Delegate.py

from instructor import OpenAISchema
from pydantic import Field
from Utilities.Log import Log, Debug, colors
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Agents.Agent import Agent
    from Agents.Agency import Agency

class Delegate(OpenAISchema):
    """
    Hand off the current action item to another specialized agent
    """

    recipient_name: str = Field(
        ...,
        description="The agent's name which is being requested for assistance",
    )
    instruction: str = Field(
        ...,
        description="Specify the task required for the recipient agent to complete. Recall the agency's plan and speak to the assistant in terms of the action items you want them to complete.",
    )
    artifact: str = Field(
        default="",
        description="The artifact to be passed to the recipient agent. This could be a file, a message, or a tool output."
    )

    def run(self, agency: 'Agency'):
        
        recipient: 'Agent' = agency.get_agent(self.recipient_name)
        current_agent: 'Agent' = agency.active_agent

        prompt = f"Agency's mission:\n"
        prompt += f"{agency.prompt}\n\n"
        prompt += f"The user has approved of the following plan:\n"
        prompt += f"{agency.plan}\n\n"
        prompt += f"I, {current_agent.name}, am seeking assistance from you {recipient.name}.\n"
        prompt = "Could you help with the following instruction please:\n"
        prompt += self.instruction

        if self.artifact != "":
            prompt += f"\n\nThe artifact we are working on is:\n"
            prompt += f"{self.artifact}\n\n"
        
        Log(colors.COMMUNICATION, f"Prompting {recipient.name}:", self.instruction)

        recipient.add_message(message=prompt)

        agency.active_agent = recipient

        current_agent.task_delegated = True

        Debug(f"{current_agent.name} is delegating to {recipient.name}: {prompt}")

        return "Delegation complete. The recipient will complete the task. No need to reply."
