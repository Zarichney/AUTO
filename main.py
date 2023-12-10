# /main.py 

from openai import OpenAI
from instructor import OpenAISchema
from Agents import RecipeAgent, UserProxyAgent, CodingAgent 
from Tools.ReadFile import ReadFile
from Tools.RequestAssistance import RequestAssistance
from Tools.CreateFile import CreateFile
from Tools.MoveFile import MoveFile
from Tools.ExecutePyFile import ExecutePyFile
from Utilities.Connection import GetKey
from Utilities.OpenAiHelper import GetCompletion
from Utilities.Log import Log, colors

# Config stuff
gpt3 = "gpt-3.5-turbo"
gpt4 = "gpt-4-1106-preview"
current_model = gpt4
openai_key = GetKey()

client = OpenAI(
    api_key=openai_key,
)

## Simple completion test:
# completion = client.chat.completions.create(
#   model=gpt3,
#   messages=[
#     {"role": "system", "content": system_message},
#     {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming"}
#   ]
# )
# print(completion.choices[0].message)

## Sample mission statement:
# Fetch the content of https://en.wikipedia.org/wiki/OpenAI and transpose this wikipedia page to a local markdown file

# Coder agent setup
code_assistant = client.beta.assistants.create(
    name=CodingAgent.name,
    instructions=CodingAgent.instructions,
    model=current_model,
    tools=[
        {"type": "function", "function": ReadFile.openai_schema},
        {"type": "function", "function": MoveFile.openai_schema},
        {"type": "function", "function": CreateFile.openai_schema},
        {"type": "function", "function": ExecutePyFile.openai_schema},
    ],
)

# User agent setup
user_proxy = client.beta.assistants.create(
    name=UserProxyAgent.name,
    instructions=UserProxyAgent.instructions,
    model=current_model,
    tools=[
        {
            "type": "function",
            "function":
            # `RequestAssistance` is a tool used by the User Proxy Agent to send messages to other agents in the group chat. 
            # It helps facilitate communication between the user and specialized agents by accurately articulating 
            # user requests and maintaining ongoing communication with the relevant agents.
            RequestAssistance.openai_schema,
        },
    ],
)

thread = client.beta.threads.create()

# This is used to tie agents and their tools
agents_and_threads = {
    "code_assistant": {
        "agent": code_assistant,
        "thread": None,
        "funcs": [ReadFile, MoveFile, CreateFile, ExecutePyFile]
    }
}

# Internal function to call the `RequestAssistance` tool. 
# Supplies the necessary internal components to operate (the agents, threads and client)
def request_assistance(recipient,message):
    result = RequestAssistance(recipient=recipient,message=message).run(agents_and_threads, client)
    return result

# Program execution
while True:
    user_message = input("User: ")

    message = GetCompletion(client, user_message, user_proxy, [request_assistance], thread)

    Log(colors.GREEN, f"{user_proxy.name}: {message}")
