# /Agents/Agent.py

import json
import openai
from openai.types.beta.assistant import Assistant

class Agent:
    def __init__(self, client:openai, assistant: Assistant, thread_id=None):
        self.client = client
        self.assistant = assistant
        self.id = assistant.id
        self.name = assistant.name
        self.description = assistant.description
        self.instructions = assistant.instructions
        self.services = assistant.metadata["services"]
        self.thread = thread_id
        self.tools = []

    @property
    def thread(self):
        if self._thread is None:
            self._thread = self.client.beta.threads.create()
            
            # Update session.json
            # Find current agent config in array of 'agents'
            # and update the thread_id with the value from thread.id
            with open("./session.json", "r") as session_file:
                session = json.load(session_file)
                for agent in session["agents"]:
                    if agent["id"] == self.id:
                        agent["thread_id"] = self._thread.id
                        break
                    
        return self._thread
