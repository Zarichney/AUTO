# /Agents/Agent.py

# Base Agent class

class Agent:
    def __init__(self, key, id, agent):
        self.key = key
        self.id = id
        self.agent = agent
        self.name = agent.name
        self.description = agent.description
        self.instructions = agent.instructions
        self.services = agent.metadata["services"]
        self.thread = None
        self.tools = []
