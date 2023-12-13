# /Agents/Agent.py

import json
import os
import time
import openai
from openai.types.beta.assistant import Assistant
from openai.types.beta.thread import Thread
from Utilities.Log import Debug, Log, colors
from Utilities.Config import current_model, session_file_name
from Tools.Plan import Plan
from Tools.Delegate import Delegate
from Tools.Inquire import Inquire
from Tools.ReadFile import ReadFile
from Tools.ExecutePyFile import ExecutePyFile
from Tools.CreateFile import CreateFile
from Tools.DownloadFile import DownloadFile
from Tools.MoveFile import MoveFile

class Agent:
    def __init__(self, client:openai, assistant:Assistant, thread:Thread=None):
        self.client = client
        if not client:
            # throw error
            raise Exception("OpenAI Client not found.")
        self.assistant = assistant
        self.id = assistant.id
        self.name = assistant.name
        self.description = assistant.description
        self.instructions = assistant.instructions
        self.services = getattr(assistant, 'metadata', {}).get("services", [])
        self.thread = thread
        self.thread_id = thread.id if thread is not None else None
        self.waiting_on_response = False
        self.task_delegated = False
        self.tools = []
        self.shared_tools = [ReadFile,CreateFile,DownloadFile,MoveFile,ExecutePyFile]
        self.internal_tools = [Plan,Delegate,Inquire]
        self.running_tool = False
        self.setup_tools()

    @property
    def thread(self):
        if self._thread is None:
            self._thread = self.client.beta.threads.create()
            self.thread_id = self._thread.id
            Debug(f"Created thread for agent {self.name} with id {self.thread_id}")
            # Update session.json
            # and update the thread_id with the value from thread.id
            with open(session_file_name, "r+") as session_file:
                session = json.load(session_file)
                for agent in session["agents"]:
                    if agent["id"] == self.id:
                        agent["thread_id"] = self.thread_id
                        break
                    
                session_file.seek(0) # Move the cursor back to the beginning of the file
                json.dump(session, session_file) # Write the updated session back to the file
                session_file.truncate() # Truncate the file to remove any leftover parts of the old content
                session_file.flush() # Ensure the changes are written to disk
                os.fsync(session_file.fileno())
                    
        return self._thread

    @thread.setter
    def thread(self, value):
        self._thread = value
    
    def add_tool(self, tool):
        self.tools.append(tool)

    def setup_tools(self):

        for tool in self.shared_tools:
            self.add_tool(tool)

        # if self.name == UserAgent.name:
        #    self.tools.append(CustomTool)


    def add_message(self, message):

        self.waiting_on_response = False

        # todo: support seed
        # appears to currently not be supported: https://github.com/openai/openai-python/blob/790df765d41f27b9a6b88ce7b8af713939f8dc22/src/openai/resources/beta/threads/messages/messages.py#L39
        # reported issue: https://community.openai.com/t/seed-param-and-reproducible-output-do-not-work/487245

        return self.client.beta.threads.messages.create(
            thread_id=self.thread.id, 
            role="user", 
            content=message,
        )

    def get_completion(self, message=None, useTools=True):

        client = self.client

        thread = self.thread

        if self.running_tool:
            completion = client.chat.completions.create(
            model=current_model,
            messages=[
                {"role": "system", "content": self.instructions},
                {"role": "user", "content": message}
            ]
            )
            response = completion.choices[0].message.content

            return response


        self.waiting_on_response = False

        if not thread:
            # throw error
            raise Exception(f"Thread for agent {self.name} not found.")

        if message is not None:
            message = self.add_message(message=message)

        # run this thread
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

                    # try:
                    self.running_tool = True
                    
                    # init tool
                    if func is None:
                        tool_names = [func.__name__ for func in self.tools]
                        raise ValueError(f"No tool found with name {tool_call.function.name}. Available tools: {', '.join(tool_names)}")
                    else:
                        arguments = tool_call.function.arguments.replace('true', 'True').replace('false', 'False')
                        tool = func(**eval(arguments))
                        
                    # get outputs from the tool
                    if isinstance(tool, str):
                        output = tool
                    else:
                        output = tool.run()

                    self.running_tool = False

                    Debug(f"Tool '{tool_call.function.name}' Completed. Reviewing tool output. Evaluating what to do next...")

                    # except Exception as e:
                    #     error_message = f"Error occurred in function '{tool_call.function.name}': {str(e)}"
                    #     error_traceback = traceback
                    #     Log(colors.ERROR, error_message)
                    #     Log(colors.ERROR, error_traceback)
                    #     output = error_message + "\n" + error_traceback

                    tool_outputs.append({"tool_call_id": tool_call.id, "output": output})

                # submit tool outputs
                run = client.beta.threads.runs.submit_tool_outputs(
                    thread_id=thread.id, run_id=run.id, tool_outputs=tool_outputs
                )

            # error
            elif run.status == "failed":
                raise Exception("Run Failed. Error: ", run.last_error)

            # return assistant message
            else:
                completion = client.beta.threads.messages.list(thread_id=thread.id)
                response = completion.data[0].content[0].text.value

                if self.task_delegated:
                    self.waiting_on_response = False
                else:
                    self.waiting_on_response = True

                return response
