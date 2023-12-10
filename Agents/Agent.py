# /Agents/Agent.py

# Base Agent class

class Agent:
    def __init__(self, key, id, agent):
        self.key = key
        self.id = id
        self.agent = agent
        self.thread = None
        self.tools = []
