# /Agents/Agent.py

import json
import openai
from openai.types.beta.assistant import Assistant
from Utilities.Config import current_model

class Agent:
    def __init__(self, client:openai, assistant: Assistant, thread_id=None):
        self.client = client
        if not client:
            # throw error
            raise Exception("OpenAI Client not found.")
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

    def get_completion(message, useTools=True):

        client = self.client

        thread = self.thread

        if not thread:
            # throw error
            raise Exception(f"Thread for agent {self.name} not found.")

        if not useTools:
            completion = client.chat.completions.create(
                model=current_model,
                messages=[
                    {"role": "system", "content": self.instructions},
                    {"role": "user", "content": message},
                ],
            )
            response = completion.choices[0].message.content

            return response

        # create new message in the thread
        message = client.beta.threads.messages.create(
            thread_id=thread.id, role="user", content=message
        )

        # run this thread
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=self.id,
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
                    Log(
                        colors.ACTION,
                        f"{self.name} is invoking tool: {tool_call.function.name}",
                    )
                    # Find the tool to be executed
                    func = next(
                        (
                            func
                            for func in self.tools
                            if func.__name__.startswith("internal_tool_")
                            or func.__name__ == tool_call.function.name.lower()
                        ),
                        None,
                    )

                    # try:
                    # init tool
                    tool = func(**eval(tool_call.function.arguments))
                    # get outputs from the tool
                    if isinstance(tool, str):
                        output = tool
                    else:
                        output = tool.run()

                    Log(
                        colors.ACTION,
                        f"Tool '{tool_call.function.name}' Completed. Evaluating what to do next...",
                    )

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

                return response
