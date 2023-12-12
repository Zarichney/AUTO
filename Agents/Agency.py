# /Agents/Agency.py

import json
import os
import openai
from openai.types.beta.assistant import Assistant
from Agents.Agent import Agent
from Agents import TeamMember, UserAgent, CodingAgent, QaAgent, RecipeAgent
from Tools.Plan import Plan
from Tools.Delegate import Delegate
from Tools.ReadFile import ReadFile
from Tools.CreateFile import CreateFile
from Tools.MoveFile import MoveFile
from Tools.ExecutePyFile import ExecutePyFile
from Utilities.Config import GetClient, current_model, session_file
from Utilities.Log import Log, Debug, colors

class Agency:
    def __init__(self, new_session: bool = False):
        self.client:openai  = GetClient()
        self.agents = []
        self.plan = None
        self.prompt = None
        self.active_agent = self.get_agent(UserAgent.name)

        self.setup(new_session)

    def setup(self, new_session: bool = False):
        # if session_file does not exist, create file and force update new_session to True
        if not os.path.exists(session_file):
            new_session = True
            with open(session_file, "w") as session_file:
                session_file.write(json.dumps({"agents": []}) + "\n")
        
        with open(session_file, "r") as session_file:
            session = json.load(session_file)

        if new_session:
            for agent_dict in session["agents"]:
                self.client.beta.assistants.delete(agent_dict["id"])
            self.create_agents()
        else:
            for agent_dict in session["agents"]:

                thread = None
                if "thread_id" in agent_dict:
                    thread = self.client.beta.threads.retrieve(agent_dict["thread_id"])

                self.add_assistant(Agent(
                    self.client,
                    self.client.beta.assistants.retrieve(agent_dict["id"]),
                    thread
                ))

    def add_assistant(self, assistant: Assistant, tools=None):
        self.agents.append(Agent(self.client, assistant))
        if tools is not None:
            for tool in tools:
                self.agents[-1].add_tool(tool)

    def get_agent(self, name):
        for agent in self.agents:
            if agent.name == name:
                return agent

        # An invalid name was supplied, use GPT to find the correct agent name
        
        list_of_agent_names = [agent.name for agent in self.agents]

        message = (
            "List of agents: "
            + ", ".join(list_of_agent_names)
            + "\n\nWhat is the actual agent name for: "
            + name
            + "\nTell me the agent name and nothing else."
        )
        
        Log(colors.ERROR, f"Agent {name} not found in agency. Engaging fall back:\n\n{message}")

        # todo use the json output for better reliability
        completion = self.client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[
                {
                    "role": "system",
                    "content": "Solve this small problem. The prompt will be provide you a list of agent names and a mismatched name. The goal is to select the closest resembling agent name based off the one provide.You must answer with only the correct agent name and nothing else.",
                },
                {
                    "role": "user",
                    "content": message,
                },
            ],
        )
        response = completion.choices[0].message.content
        
        actualAgentName = response

        Log(colors.ERROR, f"Agent name fallback determined: {actualAgentName}")

        for agent in self.agents:
            if agent.name == actualAgentName:
                return agent

        if not agent:
            Log(colors.ERROR, f"Agent {name} not found in agency.")
            return
            
        return None

    def broadcast(self, message):
        for agent in self.agents:
            if agent != self.active_agent:
                agent.add_message(message=message)

    def internal_tool_delegate(self, recipient_name, artifact, instruction):
        return Delegate(
            recipient_name=recipient_name, 
            artifact=artifact,
            instruction=instruction
            ).run(agency=self.agency)

    def internal_tool_plan(self, mission, team_planning):
        return Plan(
            mission=mission,
            team_planning = team_planning,
            ).run(agency=self.agency)
    
    def create_agents(self):
        
        team_member_instructions = TeamMember.get_team_instruction()
        
        self.add_assistant(self.client.beta.assistants.create(
            name=UserAgent.name,
            description=UserAgent.description,
            instructions=UserAgent.instructions + team_member_instructions,
            model=current_model,
            metadata={"key": "user", "services": UserAgent.services},
            tools=[
                {"type": "function", "function": Plan.openai_schema},
                {"type": "function", "function": Delegate.openai_schema},
                {"type": "function", "function": ReadFile.openai_schema},
                {"type": "function", "function": MoveFile.openai_schema},
                {"type": "function", "function": Delegate.openai_schema},
                {"type": "function", "function": ExecutePyFile.openai_schema},
            ],
        ), tools=[self.internal_tool_delegate, self.internal_tool_plan])
        
        self.add_assistant(assistant=self.client.beta.assistants.create(
            name=CodingAgent.name,
            description=CodingAgent.description,
            instructions=CodingAgent.instructions + team_member_instructions,
            model=current_model,
            metadata={"key": "coder", "services": CodingAgent.services},
            tools=[
                {"type": "function", "function": Plan.openai_schema},
                {"type": "function", "function": Delegate.openai_schema},
                {"type": "function", "function": ReadFile.openai_schema},
                {"type": "function", "function": MoveFile.openai_schema},
                {"type": "function", "function": CreateFile.openai_schema},
                {"type": "function", "function": ExecutePyFile.openai_schema},
            ],
        ), tools=[self.internal_tool_delegate, self.internal_tool_plan])
        
        # QA agent setup
        self.add_assistant(self.client.beta.assistants.create(
            name=QaAgent.name,
            description=QaAgent.description,
            instructions=QaAgent.instructions + team_member_instructions,
            model=current_model,
            metadata={"key": "qa", "services": QaAgent.services},
            tools=[
                {"type": "function", "function": Plan.openai_schema},
                {"type": "function", "function": Delegate.openai_schema},
                {"type": "function", "function": ReadFile.openai_schema},
                {"type": "function", "function": MoveFile.openai_schema},
                {"type": "function", "function": CreateFile.openai_schema},
                {"type": "function", "function": ExecutePyFile.openai_schema},
            ],
        ), tools=[self.internal_tool_delegate, self.internal_tool_plan])
        
        self.add_assistant(self.client.beta.assistants.create(
            name=RecipeAgent.name,
            description=RecipeAgent.description,
            instructions=RecipeAgent.instructions + team_member_instructions,
            model=current_model,
            metadata={"key": "recipe", "services": RecipeAgent.services},
            tools=[
                {"type": "function", "function": Plan.openai_schema},
                {"type": "function", "function": Delegate.openai_schema},
                {"type": "function", "function": ReadFile.openai_schema},
                {"type": "function", "function": MoveFile.openai_schema},
                {"type": "function", "function": CreateFile.openai_schema},
                {"type": "function", "function": ExecutePyFile.openai_schema},
            ],
        ), tools=[self.internal_tool_delegate, self.internal_tool_plan])
        
        # Store the list of assistant ids to ./session.json
        with open(session_file, "w") as session_file:
            agent_data = []
            for agent in self.agents:
                agent_data.append({
                    "id": agent.id,
                    "thread_id": agent.thread_id
                })
            session_file.write(json.dumps({"agents": agent_data}) + "\n")

    def operate(self, prompt = None):

        response = self.active_agent.get_completion(message=prompt)
        
        while self.active_agent.waiting_on_response == False:
            response = self.active_agent.get_completion()
            Debug(f"{self.active_agent.name}: {response}")
        
        return response
