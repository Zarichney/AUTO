# /Tools/ExecutePyFile.py

import subprocess
from instructor import OpenAISchema
from pydantic import Field

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