# /Tools/ExecutePyFile.py

import os
import subprocess
import sys
from instructor import OpenAISchema
from pydantic import Field
from Utilities.Log import Log, colors
import pkg_resources

class ExecutePyFile(OpenAISchema):
    """
    Run local python (.py) file.
    Execution in this environment is safe and has access to all standard Python packages and the internet.
    Only use this tool if you understand how to troubleshoot with python, if not seek delegation to a more specialized agent.
    Additional packages can be installed by specifying them in the required_packages field.
    """

    file_name: str = Field(..., description="The path to the .py file to be executed.")

    required_packages: str = Field(
        default="",                           
        description="Required packages to be installed. List of comma delimited strings. Will execute ''pip install <package>'' for each package supplied")
    
    directory: str = Field(
        default="./ai-working-dir/",
        description="The path to the directory where to file is stored. Path can be absolute or relative."
    )

    def check_dependencies(self, required_packages):
        """Check if the required modules are installed."""

        packages = required_packages.split(',')

        for package in packages:
            try:
                dist = pkg_resources.get_distribution(package)
                Log(colors.ACTION,"{} ({}) is installed".format(dist.key, dist.version))
            except pkg_resources.DistributionNotFound:
                Log(colors.ACTION,f"The {package} module is not installed. Attempting to install...")
                try:
                    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                    Log(colors.ACTION,f"Successfully installed {package}.")
                    
                except subprocess.CalledProcessError as e:
                    message = f"Failed to install {package}. Error: {e.output}"
                    Log(colors.ERROR, message)
                    return message

        return "All required modules are installed."

    def run(self):
        """Executes a Python script at the given file path and captures its output and errors."""
        
        # Check if the required modules are installed
        if self.required_packages:
            check_result = self.check_dependencies(self.required_packages)
            if check_result != "All required modules are installed.":
                return check_result
        
        # If file doesnt exist, return message
        if not os.path.exists(self.directory + self.file_name):
            return f"File {self.directory + self.file_name} does not exist."
        
        try:
            Log(colors.ACTION, f"Executing {self.file_name}...")
        
            execution = subprocess.run(
                ["python", self.directory + self.file_name], text=True, capture_output=True, check=True
            )
            
            result = f"Execution results: {execution.stdout}"
            Log(colors.RESULT, result)
            return result
        
        except subprocess.CalledProcessError as e:
            
            result = f"Execution error occurred: {e.stderr}"
            Log(colors.ERROR, result)
            return result