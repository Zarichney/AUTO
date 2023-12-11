# /Tools/RequestAssistance.py

from typing import Dict
from instructor import OpenAISchema
from pydantic import Field
from Agents.Agent import Agent
from Utilities.Helpers import GetAgent
from Utilities.OpenAiHelper import GetCompletion
from Utilities.Log import Log, colors

class RequestAssistance(OpenAISchema):
    """Send messages to other specialized agents in this group chat."""

    recipient_name: str = Field(
        ...,
        description="The agent's name which is being requested for assistance",
    )
    message: str = Field(
        ...,
        description="Specify the task required for the recipient agent to complete. Focus instead on clarifying what the task entails, rather than providing detailed instructions.",
    )

    def run(self, agency: Dict[str, Agent], client):
        # find agent by name in agency
        recipient = GetAgent(client, agency, self.recipient_name)
            
        # todo: add some prompt engineering here
        prompt = self.message
        
        thread = client.beta.threads.create()

        Log(colors.COMMUNICATION, f"Prompting {recipient.name}:", prompt)
        
        response = GetCompletion(client=client, message=prompt, agent=recipient, thread=thread)

        Log(colors.RESULT, f"{recipient.name} response:", response)
        
        response += "\n\nWhat is next in the plan?\n"
        
        return response
