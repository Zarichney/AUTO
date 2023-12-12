# /Tools/DownloadFile.py

import os
import requests
from urllib import request
from instructor import OpenAISchema
from pydantic import Field
from Utilities.Log import Log, Debug, colors

class DownloadFile(OpenAISchema):
    """Used to download a file from the internet given a url"""

    url: str = Field(
        ...,
        description="The url to download the file from",
    )
    working_dir: str = Field(
        default="./ai-working-dir/",
        description="The path to the directory to be write files to."
    )
    filename: str = Field(
        default=None,
        description="Specify a custom name to save the downloaded file as",
    )
    overwrite: str = Field(
        default=False,
        description="If true, will overwrite the file if it already exists."
    )

    def run(self):
            
        if self.filename is None:
            self.filename = self.url.split("/")[-1]

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
            
        try:
            with request.get(self.url, stream=True) as r:
                r.raise_for_status()
                with open(self.working_dir + self.file_name, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192): 
                        f.write(chunk)
        except requests.exceptions.RequestException as e:
            print(f"Error downloading file: {e}")

        Log(colors.ACTION, f"{self.url} has been downloaded to '{self.filename}'")

