# /Tools/Inquire.py

from instructor import OpenAISchema
from pydantic import Field
from Utilities.Log import Log, Debug, colors
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Agents.Agent import Agent
    from Agents.Agency import Agency

class Inquire(OpenAISchema):
    """
    Used to get information from another agent
    """

    recipient_name: str = Field(
        ...,
        description="The agent's name which is being queried",
    )
    prompt: str = Field(
        ...,
        description="The inquiry to send to the recipient agent",
    )
    chain_of_thought: str = Field(
        description="Your own chain of thought. Useful for the recipient to understand your thought process."
    )
    # useTools: bool = Field(
    #     default = False,
    #     description="Whether or not you allow the recipient to have access to their tools in order to complete the inquiry. Typically left as default false because this inquiry tool is meant for their own knowledge, however there can be the case where the recipient would require tool access to properly respond to the inquiry."
    # )

    def run(self, agency: 'Agency'):

        recipient: 'Agent' = agency.get_agent(self.recipient_name)
        current_agent: 'Agent' = agency.active_agent

        prompt = f"{recipient.name}, it is I, {current_agent.name}.\n"
        prompt += "I have an inquiry for you:\n\n"
        prompt += f"{self.prompt}\n\n"
        
        prompt += f"My chain of thought is:\n"
        prompt += f"{self.chain_of_thought}\n\n"

        prompt += "Could you share what you think step by step?\n"

        Log(colors.COMMUNICATION, f"{current_agent.name} is inquiring to {recipient.name}:\n{self.prompt}")
        Debug(f"{current_agent.name} used inquiry tool on {recipient.name}. Full prompt:\n{prompt}")

        response = recipient.get_completion(message=prompt, useTools=False)

        Log(colors.COMMUNICATION, f"{recipient.name} response to {current_agent.name}:\n{response}")

        return f"{recipient.name}:\n{response}"

