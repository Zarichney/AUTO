# /Tools/RequestAssistance.py

from typing import Dict
from instructor import OpenAISchema
from pydantic import Field
from Agents.Agent import Agent
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
        recipient = next((agent for agent in agency.values() if agent.name == self.recipient_name), None)
        
        if not recipient:
            Log(colors.RED, f"Agent {self.recipient_name} not found in agency.")
            return
        
        # if there is no thread between user proxy and this agent, create one
        if not recipient.thread:
            recipient.thread = client.beta.threads.create()
            
        Log(colors.CYAN, f"Prompting {recipient.name}:", self.message)

        message = GetCompletion(client=client, message=self.message, agent=recipient)

        Log(colors.CYAN, f"{recipient.name} response:", message)
        
        return message
    
    
    
    

## Simple completion test:
# completion = client.chat.completions.create(
#   model=gpt3,
#   messages=[
#     {"role": "system", "content": system_message},
#     {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming"}
#   ]
# )
# print(completion.choices[0].message)