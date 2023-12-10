# /Tools/CreateFile.py

from instructor import OpenAISchema
from pydantic import Field

class CreateFile(OpenAISchema):
    """
    Python file with a succinct appropriate name and a version number that represents the iteration. Containing code that can be saved and executed locally at a later time. This environment has access to all standard Python packages and the internet.
    """
    chain_of_thought: str = Field(
        ...,
        description="Think step by step to determine the correct actions that are needed to be taken in order to complete the task.",
    )
    file_name: str = Field(
        ..., description="The name of the file including the extension"
    )
    working_dir: str = Field(
        default="./ai-working-dir/",
        description="The path to the directory to be write files to."
    )
    body: str = Field(..., description="Correct contents of a file")

    def run(self):
        with open(self.working_dir + self.file_name, "w") as f:
            f.write(self.body)

        return "File written to " + self.file_name