import sys
from Agency import Agency
from Utilities.Log import Log, type

agency:Agency = Agency()

if len(sys.argv) == 1:
    Log(type.PROMPT, f"AUTO Agency: How can I help?\n\n>")

# If user didn't supply prompt as part of program call, wait for input
user_message = sys.argv[1] if len(sys.argv) > 1 else input()

agency.complete(
    mission_prompt=user_message,
    single_agent=False,
    stop_word="exit",
    continue_phrase="terminate",
)
