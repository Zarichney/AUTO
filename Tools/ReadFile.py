# /Tools/ReadFile.py

from instructor import OpenAISchema
from pydantic import Field

class ReadFile(OpenAISchema):
    """
    Read the contents of a local file.
    """
    file_name: str = Field(
        ..., description="The name of the file including the extension"
    )
    directory: str = Field(
        default="./",
        description="The path to the directory where to file is stored. Path can be absolute or relative."
    )
    body: str = Field(..., description="Correct contents of a file")

    def run(self):
        with open(self.directory + self.file_name, "r") as f:
            file_content = f.read()

        return file_content