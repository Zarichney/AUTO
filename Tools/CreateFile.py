# /Tools/CreateFile.py

import os
from instructor import OpenAISchema
from pydantic import Field
from Utilities.Log import Log, colors

class CreateFile(OpenAISchema):
    """
    Tool to create a file with with an extension. 
    If this is a temporary file, it can simply be created at the default location of ./ai-working-dir/. Alternatively a file can be created at a specified location.
    Overwriting is not the default behavior. It is encouraged to always created a new file with a unique name.
    """
    
    file_name: str = Field(
        ..., 
        description="The name of the file including the extension"
    )
    working_dir: str = Field(
        default="./ai-working-dir/",
        description="The path to the directory to be write files to."
    )
    body: str = Field(
        ...,
        description="The actual contents contents of a file"
    )
    overwrite: str = Field(
        default=False,
        description="If true, will overwrite the file if it already exists."
    )

    def run(self):
        
        # If file already exists, return message
        if os.path.exists(self.working_dir + self.file_name):
            if self.overwrite:
                Log(colors.ACTION, f"Overwriting file: {self.working_dir + self.file_name}")
            else:
                result = f"File {self.working_dir + self.file_name} already exists.\n"
                result += "Specify to overwrite if you this is intended, or\n"
                result += "increment the file version for a unique file name"
                Log(colors.ERROR, result)
                return result
        
        # Create directory if it doesnt exist already
        if not os.path.exists(self.working_dir):
            Log(colors.ACTION, f"Creating directory: {self.working_dir}")
            os.makedirs(self.working_dir)
        
        # Write file
        with open(self.working_dir + self.file_name, "w") as f:
            f.write(self.body)
            
        result = "File written to: " + self.file_name
        Log(colors.RESULT, result)
        return result