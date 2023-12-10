import subprocess
from typing import Literal
from instructor import OpenAISchema
from pydantic import Field
from utils import wprint, bcolors, get_completion

class ExecutePyFile(OpenAISchema):
    """Run existing python file from local disc."""

    file_name: str = Field(..., description="The path to the .py file to be executed.")
    working_dir: str = "./ai-working-dir/"

    def run(self):
        """Executes a Python script at the given file path and captures its output and errors."""
        try:
            result = subprocess.run(
                ["python", self.working_dir + self.file_name], text=True, capture_output=True, check=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            return f"An error occurred: {e.stderr}"
          
          
class ReviewDirectory(OpenAISchema):
    """
    Review the contents of a directory in order to determine whether there exist a python script to use.
    When finding multiple potential scripts, use the latest one.
    """
    chain_of_thought: str = Field(
        ...,
        description="Think step by step to determine the correct actions that are needed to be taken in order to complete the task.",
    )
    working_dir: str = Field(
        default="./ai-working-dir/",
        description="The path to the directory to be reviewed."
    )
    
    def run(self):
        """Review the contents of a directory in order to determine whether there exist a python script to use.
        When finding multiple potential scripts, use the latest one.
        """
        import os
        import re
        import glob

        # get all files in the directory
        files = glob.glob(self.working_dir + "*.py")

        # filter out files that do not match the pattern
        files = [file for file in files if re.match(r".*v\d+\.py", file)]

        # sort files by version
        files = sorted(files, key=lambda file: int(re.findall(r"v(\d+)\.py", file)[0]))

        # get the latest file
        file = files[-1]

        return file

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
      
class SendMessage(OpenAISchema):
    """Send messages to other specialized agents in this group chat."""

    recipient: Literal["code_assistant"] = Field(
        ...,
        description="code_assistant is a world class programming AI capable of executing python code.",
    )
    message: str = Field(
        ...,
        description="Specify the task required for the recipient agent to complete. Focus instead on clarifying what the task entails, rather than providing detailed instructions.",
    )

    def run(self, agents_and_threads, client):
        recipient = agents_and_threads[self.recipient]
        # if there is no thread between user proxy and this agent, create one
        if not recipient["thread"]:
            recipient["thread"] = client.beta.threads.create()
            
        wprint(bcolors.CYAN, f"Prompting {recipient['agent'].name}:", self.message)

        message = get_completion(client=client, message=self.message, **recipient)

        wprint(bcolors.CYAN, f"{recipient['agent'].name} response:", message)
        
        return message