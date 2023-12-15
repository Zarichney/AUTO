# /Agents/Agent.py

import time
import openai
from openai.types.beta.assistant import Assistant
from openai.types.beta.thread import Thread
from Utilities.Log import Debug, Log, colors
from Utilities.Config import current_model
from Tools.Plan import Plan
from Tools.Delegate import Delegate
from Tools.Inquire import Inquire
from Tools.ReadFile import ReadFile
from Tools.ExecutePyFile import ExecutePyFile
from Tools.GetDirectoryContents import GetDirectoryContents
from Tools.RecipeScraper.RecipeScaper import RecipeScaper
from Tools.CreateFile import CreateFile
from Tools.DownloadFile import DownloadFile
from Tools.MoveFile import MoveFile
from Agents import RecipeAgent

class Agent:
    def __init__(self, assistant:Assistant, agency, thread:Thread):
        if not assistant:
            raise Exception("Assistant not supplied")
        if not agency:
            raise Exception("OpenAI Client not found.")
        if not thread:
            raise Exception("Thread required")
        
        self.assistant:Assistant = assistant
        self.agency = agency
        self.thread:Thread = thread

        self.id = self.assistant.id
        self.name = self.assistant.name
        self.description = self.assistant.description
        self.instructions = self.assistant.instructions
        self.services = getattr(self.assistant, 'metadata', {}).get("services", [])

        self.waiting_on_response = False
        self.task_delegated = False

        self.tools = []
        self.shared_tools = [ReadFile,CreateFile,DownloadFile,MoveFile,ExecutePyFile,GetDirectoryContents]
        self.internal_tools = [Plan,Delegate,Inquire]
        self.setup_tools()
    
    def add_tool(self, tool):
        self.tools.append(tool)

    def setup_tools(self):

        for tool in self.shared_tools:
            self.add_tool(tool)

        if self.name == RecipeAgent.name:
           self.tools.append(RecipeScaper)

    def get_completion(self, message=None, useTools=True):

        client = self.agency.client
        thread = self.thread

        if self.agency.running_tool:
            Debug(f"Agent called for completion while it's currently waiting on tool usage to complete. Falling back to thread-less completion")
            return client.chat.completions.create(
                model=current_model,
                messages=[
                    {"role": "system", "content": self.instructions},
                    {"role": "user", "content": message}
                ]
            ).choices[0].message.content
        else:
            # Messages can't be added while a tool is running so they get queued up
            # Unload message queue
            for queued_message in self.agency.message_queue:
                self.agency.add_message(message=queued_message)
            self.agency.message_queue = []

        self.waiting_on_response = False

        if message is not None:
            message = self.agency.add_message(message=message)

        # run creation
        if useTools:
            run = client.beta.threads.runs.create(
                thread_id=thread.id,
                assistant_id=self.id,
            )
        else:
            run = client.beta.threads.runs.create(
                thread_id=thread.id,
                assistant_id=self.id,
                tools=[] # forces assistant to respond with prompt
            )

        while True:
            # wait until run completes
            while run.status in ["queued", "in_progress"]:
                run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
                time.sleep(1)

            # function execution
            if run.status == "requires_action":
                tool_calls = run.required_action.submit_tool_outputs.tool_calls
                tool_outputs = []
                for tool_call in tool_calls:
                    Debug(f"{self.name} is invoking tool: {tool_call.function.name}")
                    # Find the tool to be executed
                    func = next(
                        (
                            func
                            for func in self.tools
                            if func.__name__.replace("internal_tool_", "").lower() == tool_call.function.name.lower()
                        ),
                        None,
                    )
                    
                    # init tool
                    if func is None:
                        tool_names = [func.__name__ for func in self.tools]
                        Log(colors.ERROR, f"No tool found with name {tool_call.function.name}. Available tools: {', '.join(tool_names)}")
                        output = f"{tool_call.function.name} is not a valid tool name. Available tools: {', '.join(tool_names)}"
                        
                    else:
                        self.agency.running_tool = True
                        try:
                            
                            arguments = tool_call.function.arguments.replace('true', 'True').replace('false', 'False')
                            tool = func(**eval(arguments))
                            
                            if isinstance(tool, str):
                                output = tool
                            else:
                                output = tool.run()

                            Debug(f"Tool '{tool_call.function.name}' Completed. Reviewing tool output. Evaluating what to do next...")

                        except Exception as e:
                            Log(colors.ERROR, f"Error occurred in function '{tool_call.function.name}': {str(e)}")
                            output = f"Tool '{tool_call.function.name}' failed. Error: {str(e)}"
                        self.agency.running_tool = False

                    tool_outputs.append({"tool_call_id": tool_call.id, "output": output})

                # submit tool outputs
                run = client.beta.threads.runs.submit_tool_outputs(
                    thread_id=thread.id, run_id=run.id, tool_outputs=tool_outputs
                )

            # error
            elif run.status == "failed":
                Log(colors.ERROR, f"Run Failed. Error: {run.last_error}")
                Debug(f"Run {run.id} has been cancelled")
                return "An internal server error occurred. Try again"

            # return assistant response
            else:
                completion = client.beta.threads.messages.list(thread_id=thread.id)
                response = completion.data[0].content[0].text.value

                if self.task_delegated:
                    self.waiting_on_response = False
                else:
                    self.waiting_on_response = True

                return response
