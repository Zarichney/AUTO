from openai import OpenAI
from agents import RecipeAgent, UserProxyAgent, CodingAgent 
from tools import ExecutePyFile, ReviewDirectory, CreateFile, SendMessage
from utils import wprint, bcolors, get_completion

# Config stuff
gpt3 = "gpt-3.5-turbo"
gpt4 = "gpt-4-1106-preview"
current_model = gpt4
openai_key = ""

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
        {"type": "function", "function": ReviewDirectory.openai_schema},
        {"type": "function", "function": CreateFile.openai_schema},
        {"type": "function", "function": ExecutePyFile.openai_schema},
    ],
)

# User agent setup
user_proxy = client.beta.assistants.create(
    name=RecipeAgent.name + " / " + UserProxyAgent.name,
    instructions=RecipeAgent.instructions + " / " + UserProxyAgent.instructions,
    model=current_model,
    tools=[
        {
            "type": "function",
            "function":
            # `SendMessage` is a tool used by the User Proxy Agent to send messages to other agents in the group chat. 
            # It helps facilitate communication between the user and specialized agents by accurately articulating 
            # user requests and maintaining ongoing communication with the relevant agents.
            SendMessage.openai_schema,
        },
    ],
)

thread = client.beta.threads.create()

# This is used to tie agents and their tools
agents_and_threads = {
    "code_assistant": {
        "agent": code_assistant,
        "thread": None,
        "funcs": [ReviewDirectory, CreateFile, ExecutePyFile]
    }
}

# Internal function to call the `SendMessage` tool. 
# Supplies the necessary internal components to operate (the agents, threads and client)
def send_message(recipient,message):
    result = SendMessage(recipient=recipient,message=message).run(agents_and_threads, client)
    return result

# Program execution
while True:
    user_message = input("User: ")

    message = get_completion(client, user_message, user_proxy, [send_message], thread)

    wprint(bcolors.GREEN, f"{user_proxy.name}: {message}")
