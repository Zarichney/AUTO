# /Utilities/Log.py

import textwrap

DEBUGGING_ENABLED = True

class style:
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

class colors:
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    RESET = "\033[0m"
    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"

class type:
    DEBUG = colors.BRIGHT_MAGENTA
    COMMUNICATION = colors.BRIGHT_CYAN
    RESULT = colors.GREEN
    PROMPT = colors.WHITE
    ACTION = colors.YELLOW
    ERROR = colors.RED

def Debug(*args, **kwargs):
    if DEBUGGING_ENABLED:
        Log(type.DEBUG, *args, **kwargs)


def Log(color, *args, width=None, **kwargs):
    """
    Custom print function that wraps text to a specified width.

    Args:
    *args: Variable length argument list.
    width (int): The maximum width of wrapped lines. If None, no line wrapping will be performed.
    **kwargs: Arbitrary keyword arguments.
    """
    if width is not None:
        wrapper = textwrap.TextWrapper(width=width)

        # Process all arguments to make sure they are strings and wrap them
        wrapped_args = [wrapper.fill(str(arg)) for arg in args]

        # Print the wrapped text in the specified color
        print(color + '\n' + ' '.join(wrapped_args) + "\n" + style.ENDC, **kwargs)
    else:
        # Print the text without line wrapping in the specified color
        print(color + '\n' + ' '.join(args) + "\n" + style.ENDC, **kwargs)
