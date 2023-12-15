# /Tools/GetDirectoryContents.py

import os
import time
from instructor import OpenAISchema
from pydantic import Field
from Utilities.Log import Log, colors

class GetDirectoryContents(OpenAISchema):
    """
    List all files within a given directory
    """

    directory: str = Field(
        ...,
        description="The path to the directory to be read"
    )

    def run(self):

        if not os.path.exists(self.directory):
            result = f"Directory does not exist: {self.directory}"
            Log(colors.ERROR, result)
            return result
        
        # Get a list of filenames in the directory
        filenames = os.listdir(self.directory)

        # Get the last modification date and size for each file
        file_info = [(filename, time.ctime(os.path.getmtime(os.path.join(self.directory, filename))), os.path.getsize(os.path.join(self.directory, filename))) for filename in filenames]

        # Format the output as a Markdown table
        listing = "| Filename | Size (bytes) Last Modified | |\n"
        listing += "| --- | --- | --- |\n"
        for filename, size, last_modified in file_info:
            listing += f"| {filename} | {size} | {last_modified} |\n"
            
        # Get the count of files
        file_count = len(filenames)
        listing += f"\nTotal number of files: {file_count}"

        Log(colors.ACTION, f"Listing files in directory: {self.directory}.\nFile Count: {file_count}")

        return listing

