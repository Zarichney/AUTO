# /Utilities/Log.py

import textwrap

class colors:
    HEADER = "\033[95m"
    DEBUG = "\033[94m"
    COMMUNICATION = "\033[96m"
    RESULT = "\033[92m"
    ACTION = "\033[93m"
    ERROR = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

debugging_enabled = True

def Debug(*args, **kwargs):
    if debugging_enabled:
        Log(colors.DEBUG, *args, **kwargs)


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
        print(color + '\n' + ' '.join(wrapped_args) + "\n" + colors.ENDC, **kwargs)
    else:
        # Print the text without line wrapping in the specified color
        print(color + '\n' + ' '.join(args) + "\n" + colors.ENDC, **kwargs)
