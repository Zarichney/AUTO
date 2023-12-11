# /Tools/MoveFile.py

import os
from instructor import OpenAISchema
from pydantic import Field
from Utilities.Log import Log, colors


class MoveFile(OpenAISchema):
    """
    Move a file from one directory to another.
    """

    file_name: str = Field(
        ..., description="The name of the file including the extension"
    )
    directory: str = Field(
        default="./ai-working-dir/",
        description="The path to the directory where to file is stored. Path can be absolute or relative.",
    )
    destination: str = Field(
        description="The path to the directory where to file is be moved to. Path can be absolute or relative."
    )
    body: str = Field(..., description="Correct contents of a file")

    def run(self):
        # If file doesnt exist, return message
        if not os.path.exists(self.directory + self.file_name):
            return f"File {self.directory + self.file_name} does not exist."

        file_destination_path = os.path.join(self.destination, self.file_name)
        os.rename(self.directory + self.file_name, file_destination_path)

        result = f"File moved to: {file_destination_path}"
        Log(colors.RESULT, result)
        return result
