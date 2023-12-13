# /Agents/Agency.py

import json
import os
import openai
from openai.types.beta.assistant import Assistant
from Agents.Agent import Agent
from Agents import TeamMember, UserAgent, CodingAgent, QaAgent, RecipeAgent
from Tools.Plan import Plan
from Tools.Delegate import Delegate
from Tools.Inquire import Inquire
from Tools.ReadFile import ReadFile
from Tools.CreateFile import CreateFile
from Tools.DownloadFile import DownloadFile
from Tools.MoveFile import MoveFile
from Tools.ExecutePyFile import ExecutePyFile
from Utilities.Config import GetClient, current_model, session_file_name
from Utilities.Log import Log, Debug, colors

class Agency:
    def __init__(self, prompt, new_session: bool = False):
        self.client:openai  = GetClient()
        self.agents = []
        self.plan = None
        self.prompt = prompt
        self.active_agent:Agent = None
        self.setup(new_session)
        
    def setup(self, new_session: bool = False):

        sessions = []
        current_session = None
        session_agents = []

        # if session_file does not exist or has empty contents, create session file and force update new_session to True
        if not os.path.exists(session_file_name) or os.stat(session_file_name).st_size == 0:
            new_session = True
            # Session file has the following structure {sessions: [{prompt: "", thread_id: "", agents: [{agent_id: ""}]}]}
            with open(session_file_name, "w") as session_file:
                session_file.write(json.dumps({"sessions": []}) + "\n")
            Debug("Created session file")
        
        # Load whatever is in the session file
        with open(session_file_name, "r") as session_file:
            sessions = json.load(session_file)["sessions"]

        if new_session == False:
            for session in sessions:
                # Existing session are matched on user prompt
                if session["prompt"] == self.prompt:
                    current_session = session
            if current_session is None:
                Debug("No session found in file")
            else:
                Debug("Loaded session from file")
                session_agents = current_session["agents"]
                thread_id = current_session["thread_id"]
                if thread_id:
                    try:
                        self.thread = self.client.beta.threads.retrieve(thread_id)
                        Debug("Thread retrieved")
                    except Exception as e:
                        self.thread = None
        
        # If we aren't able to retrieve the thread at this point, it is considered a new session
        if self.thread is None:
            new_session = True

        if new_session:
            Debug("Creating new session")

            if self.thread is not None:
                self.client.beta.threads.delete(self.thread.id)
            self.thread = self.client.beta.threads.create()

            for session_agent in session_agents:
                agent_id = session_agent["agent_id"]
                if agent_id:
                    self.client.beta.assistants.delete(agent_id)

            session = {
                "prompt": self.prompt,
                "thread_id": self.thread.id,
                "agents": []
            }

            # newly created agents in self.agents
            self.generate_agents()

            # extract out agent.id from self.agents array and for each add {agent_id: agent.id} to session["agents"]
            for agent in self.agents:
                session["agents"].append({"agent_id": agent.id})
            
            # add session to sessions
            sessions.append(session)

            # write to session file
            with open(session_file_name, "w") as session_file:
                session_file.write(json.dumps({"sessions": sessions}) + "\n")
            Debug("New session written to file")

        else:
            Debug("Retrieving agents")
            for session_agent in session["agents"]:
                agent_id = session_agent["agent_id"]
                if agent_id:
                    self.create_agent(
                        assistant=self.client.beta.assistants.retrieve(agent_id),
                        internalTools=[self.internal_tool_delegate, self.internal_tool_plan, self.internal_tool_inquire]
                    )

                # Agent creation expected. Return error if agent_id cannot be found
                if agent_id not in [agent.id for agent in self.agents]:
                    raise Exception(f"Session Loading Error: Agent with id {agent_id} could not be added to agency.")

        Debug("Agency Setup Complete")

    def create_agent(self, assistant: Assistant, internalTools=None):
        agent = Agent(self.client, assistant, self.thread)
        if internalTools is not None:
            for tool in internalTools:
                agent.add_tool(tool)
        self.agents.append(agent)

    def get_agent(self, name) -> Agent:
        for agent in self.agents:
            if agent.name == name:
                return agent

        # An invalid name was supplied, use GPT to find the correct agent name
        Log(colors.ERROR, f"Agent named '{name}' not found in agency. Engaging fall back...")
        
        list_of_agent_names = [agent.name for agent in self.agents]
        Log(colors.ERROR, f"Actual agent names: '{"', '".join(list_of_agent_names)}'")

        # todo use the json output for better reliability
        completion = self.client.chat.completions.create(
            model="gpt-4-1106-preview",
            response_format={"type:":"json_object"},
            messages=[
                {
                    "role": "system",
                    "content": """
                        Solve this problem: The prompt will be provide you a list of valid agent names and an invalid name. 
                        The goal is to identify the closest resembling valid agent name.
                        Respond using the following format: {"Name": "User agent"}
                    """,
                },
                {"role": "user", "content": f"List of agents: {", ".join(list_of_agent_names)}\nWhat is the intended valid agent name for:\n{name}"},
            ],
        )
        
        actualAgentName = json.loads(completion.choices[0].message.content)["Name"]
        Log(colors.ERROR, f"Agent name fallback determined: {actualAgentName}")

        for agent in self.agents:
            if agent.name == actualAgentName:
                return agent

        Log(colors.ERROR, f"Agent could still not be found in agency... Returning user agent")
        return self.get_agent(UserAgent.name)
    
    def UpdatePlan(self,plan):
        # todo
        self.plan = plan

    def broadcast(self, message):
        for agent in self.agents:
            if agent != self.active_agent:
                agent.add_message(message=message)

    def internal_tool_delegate(self, recipient_name, instruction, artifact=""):
        return Delegate(
            recipient_name=recipient_name, 
            instruction=instruction,
            artifact=artifact
            ).run(agency=self)

    def internal_tool_plan(self, mission):
        return Plan(
            mission=mission,
            ).run(agency=self)

    def internal_tool_inquire(self, recipient_name, prompt, chain_of_thought):
        return Inquire(
            recipient_name=recipient_name,
            prompt=prompt,
            chain_of_thought=chain_of_thought,
            ).run(agency=self)
    
    def generate_agents(self):
        
        team_member_instructions = TeamMember.get_team_instruction()
        
        self.create_agent(self.client.beta.assistants.create(
            name=UserAgent.name,
            description=UserAgent.description,
            instructions=UserAgent.instructions + team_member_instructions,
            model=current_model,
            metadata={"services": UserAgent.services},
            tools=[
                {"type": "function", "function": Plan.openai_schema},
                {"type": "function", "function": Delegate.openai_schema},
                {"type": "function", "function": Inquire.openai_schema},
                {"type": "function", "function": ReadFile.openai_schema},
                {"type": "function", "function": MoveFile.openai_schema},
                {"type": "function", "function": DownloadFile.openai_schema},
                {"type": "function", "function": ExecutePyFile.openai_schema},
            ],
        ), internalTools=[self.internal_tool_delegate, self.internal_tool_plan, self.internal_tool_inquire])
        
        self.create_agent(assistant=self.client.beta.assistants.create(
            name=CodingAgent.name,
            description=CodingAgent.description,
            instructions=CodingAgent.instructions + team_member_instructions,
            model=current_model,
            metadata={"services": CodingAgent.services},
            tools=[
                {"type": "function", "function": Plan.openai_schema},
                {"type": "function", "function": Delegate.openai_schema},
                {"type": "function", "function": Inquire.openai_schema},
                {"type": "function", "function": ReadFile.openai_schema},
                {"type": "function", "function": MoveFile.openai_schema},
                {"type": "function", "function": CreateFile.openai_schema},
                {"type": "function", "function": DownloadFile.openai_schema},
                {"type": "function", "function": ExecutePyFile.openai_schema},
            ],
        ), internalTools=[self.internal_tool_delegate, self.internal_tool_plan, self.internal_tool_inquire])
        
        # QA agent setup
        self.create_agent(self.client.beta.assistants.create(
            name=QaAgent.name,
            description=QaAgent.description,
            instructions=QaAgent.instructions + team_member_instructions,
            model=current_model,
            metadata={"services": QaAgent.services},
            tools=[
                {"type": "function", "function": Plan.openai_schema},
                {"type": "function", "function": Delegate.openai_schema},
                {"type": "function", "function": Inquire.openai_schema},
                {"type": "function", "function": ReadFile.openai_schema},
                {"type": "function", "function": MoveFile.openai_schema},
                {"type": "function", "function": CreateFile.openai_schema},
                {"type": "function", "function": DownloadFile.openai_schema},
                {"type": "function", "function": ExecutePyFile.openai_schema},
            ],
        ), internalTools=[self.internal_tool_delegate, self.internal_tool_plan, self.internal_tool_inquire])
        
        self.create_agent(self.client.beta.assistants.create(
            name=RecipeAgent.name,
            description=RecipeAgent.description,
            instructions=RecipeAgent.instructions + team_member_instructions,
            model=current_model,
            metadata={"services": RecipeAgent.services},
            tools=[
                {"type": "function", "function": Plan.openai_schema},
                {"type": "function", "function": Delegate.openai_schema},
                {"type": "function", "function": Inquire.openai_schema},
                {"type": "function", "function": ReadFile.openai_schema},
                {"type": "function", "function": MoveFile.openai_schema},
                {"type": "function", "function": CreateFile.openai_schema},
                {"type": "function", "function": DownloadFile.openai_schema},
                {"type": "function", "function": ExecutePyFile.openai_schema},
            ],
        ), internalTools=[self.internal_tool_delegate, self.internal_tool_plan, self.internal_tool_inquire])
        
        # Store the list of assistant ids to ./session.json
        with open(session_file_name, "w") as session_file:
            agent_data = []
            for agent in self.agents:
                agent_data.append({
                    "id": agent.id,
                    "thread_id": agent.thread_id if agent.thread_id else ""
                })
            session_file.write(json.dumps({"agents": agent_data}) + "\n")

    def operate(self):
        
        # Trigger the initial delegation
        self.active_agent.get_completion()

        while self.active_agent.waiting_on_response == False:
            
            Debug(f"active_agent.name: {self.active_agent.name}")
            Debug(f"active_agent.waiting_on_response: {self.active_agent.waiting_on_response}")
            Debug(f"active_agent.task_delegated: {self.active_agent.task_delegated}")
            
            active_agent_name = self.active_agent.name
            
            Debug("before get_completion()")
            response = self.active_agent.get_completion()
            Debug(f"after get_completion()\n{response}")
            
            previous_agent = self.get_agent(active_agent_name)
            Debug(f"previous_agent.name: {previous_agent.name}")
            Debug(f"previous_agent.waiting_on_response: {previous_agent.waiting_on_response}")
            Debug(f"previous_agent.task_delegated: {previous_agent.task_delegated}")
            
            Debug(f"active_agent.name: {self.active_agent.name}")
            Debug(f"active_agent.waiting_on_response: {self.active_agent.waiting_on_response}")
            Debug(f"active_agent.task_delegated: {self.active_agent.task_delegated}")
            
            if previous_agent.task_delegated == True and self.active_agent.name != previous_agent.name:
                # Turn this flag off now that it's been delegated
                previous_agent.task_delegated == False
            
            elif previous_agent.task_delegated == False and active_agent_name != UserAgent.name:
                Debug(f"{active_agent_name} has provided a response:\n{response}")
                # Get user agent to handle the response
                user_agent = self.get_agent(UserAgent.name)
                self.active_agent.waiting_on_response = False
                self.active_agent = user_agent
                prompt = f"{response}\n\n In regards to the overall plan. What do we do now leader?"
                user_agent_response = user_agent.get_completion(message=prompt)
                Debug(f"User agent is expected to have delegated.\nThis was its response: {user_agent_response}")
                Debug(f"The new active agent is: {self.active_agent.name}")
                # The user agent response shouldnt matter as its the instruction to say it finished delegating
                # But now a message has been dropped on the thread of the new delegate
                # And the loop will restart, causing the delegate to react to the user agent's command to continue the mission
        
        Debug(f"{self.active_agent.name} is returning back to the user with: {response}")
        return response
