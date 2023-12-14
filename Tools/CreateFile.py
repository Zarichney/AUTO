# /Tools/CreateFile.py

import os
from instructor import OpenAISchema
from pydantic import Field
from Utilities.Log import Log, colors

class CreateFile(OpenAISchema):
    """
    Tool to create a file. Supply the file name with an extension and the contents of the file.
    """
    
    file_name: str = Field(
        ..., 
        description="The name of the file including the extension"
    )
    directory: str = Field(
        default="./ai-working-dir/",
        description="The path to the directory to be write files to."
    )
    file_content: str = Field(
        ...,
        description="The full contents of the file. Do not supply a partial file."
    )
    overwrite: bool = Field(
        default=False,
        description="If true, will overwrite the file if it already exists."
    )

    def run(self):
        
        # If file already exists, return message
        if os.path.exists(self.directory + self.file_name):
            if self.overwrite:
                Log(colors.ACTION, f"Overwriting file: {self.directory + self.file_name}")
            else:
                result = f"File {self.directory + self.file_name} already exists.\n"
                result += "Specify to overwrite if you this is intended, or\n"
                result += "increment the file version for a unique file name"
                Log(colors.ERROR, result)
                return result
        
        # Create directory if it doesnt exist already
        if not os.path.exists(self.directory):
            Log(colors.ACTION, f"Creating directory: {self.directory}")
            os.makedirs(self.directory)
        
        # Write file
        with open(self.directory + self.file_name, "w") as f:
            f.write(self.file_content)
            
        result = "File written to: " + self.file_name
        Log(colors.RESULT, result)
        return result