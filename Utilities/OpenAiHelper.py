# /Utilities/OpenAiHelper.py

import time
from Utilities.Log import Log, colors

def GetCompletion(client, message, agent, funcs, thread):
    """
    Executes a thread based on a provided message and retrieves the completion result.

    This function submits a message to a specified thread, triggering the execution of an array of functions
    defined within a func parameter. Each function in the array must implement a `run()` method that returns the outputs.

    Parameters:
    - message (str): The input message to be processed.
    - agent (OpenAI Assistant): The agent instance that will process the message.
    - funcs (list): A list of function objects, defined with the instructor library.
    - thread (Thread): The OpenAI Assistants API thread responsible for managing the execution flow.

    Returns:
    - str: The completion output as a string, obtained from the agent following the execution of input message and functions.
    """

    # create new message in the thread
    message = client.beta.threads.messages.create(
        thread_id=thread.id, role="user", content=message
    )

    # run this thread
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=agent.id,
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
                Log(colors.YELLOW, f"{agent.name} is calling function {tool_call.function.name}")
                # find the tool to be executed
                func = next(
                    iter(
                        [
                            func
                            for func in funcs
                            if func.__name__.replace("_", "").lower() == tool_call.function.name.lower()
                        ]
                    )
                )

                try:
                    # init tool
                    tool = func(**eval(tool_call.function.arguments))
                    # get outputs from the tool
                    if isinstance(tool, str):
                        output = tool
                    else:
                        output = tool.run()
                except Exception as e:
                    output = "Error: " + str(e)

                Log(colors.YELLOW, f"Tool '{tool_call.function.name}' Output: ", output)
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
            messages = client.beta.threads.messages.list(thread_id=thread.id)
            message = messages.data[0].content[0].text.value
            
            return message