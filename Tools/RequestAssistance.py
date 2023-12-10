# /Tools/RequestAssistance.py

from typing import Literal
from instructor import OpenAISchema
from pydantic import Field
from Utilities.OpenAiHelper import GetCompletion
from Utilities.Log import Log, colors

class RequestAssistance(OpenAISchema):
    """Send messages to other specialized agents in this group chat."""

    recipient: Literal["code_assistant"] = Field(
        ...,
        description="code_assistant is a world class programming AI capable of executing python code.",
    )
    message: str = Field(
        ...,
        description="Specify the task required for the recipient agent to complete. Focus instead on clarifying what the task entails, rather than providing detailed instructions.",
    )

    def run(self, agents_and_threads, client):
        recipient = agents_and_threads[self.recipient]
        # if there is no thread between user proxy and this agent, create one
        if not recipient["thread"]:
            recipient["thread"] = client.beta.threads.create()
            
        Log(colors.CYAN, f"Prompting {recipient['agent'].name}:", self.message)

        message = GetCompletion(client=client, message=self.message, **recipient)

        Log(colors.CYAN, f"{recipient['agent'].name} response:", message)
        
        return message