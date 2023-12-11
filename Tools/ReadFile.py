# /Tools/ReadFile.py

import os
from instructor import OpenAISchema
from pydantic import Field

from Utilities.Log import Log, colors

class ReadFile(OpenAISchema):
    """
    Read the contents of a local file.
    """
    file_name: str = Field(
        ..., description="The name of the file including the extension"
    )
    directory: str = Field(
        default="./ai-working-dir/",
        description="The path to the directory where to file is stored. Path can be absolute or relative."
    )

    def run(self):
        
        # If file doesnt exist, return message
        if not os.path.exists(self.directory + self.file_name):
            result = f"File {self.directory + self.file_name} does not exist."
            Log(colors.ERROR, result)
            return result
        
        Log(colors.ACTION, f"Viewing content of file: {self.directory + self.file_name}")
        
        with open(self.directory + self.file_name, "r") as f:
            file_content = f.read()

        return f"File contents:\n{file_content}"