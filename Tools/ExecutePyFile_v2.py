# /Tools/ExecutePyFile_v2.py

import os
import subprocess
import sys
from instructor import OpenAISchema
from pydantic import Field
from Utilities.Log import Log, colors
import pkg_resources

# Test case import
import requests


# Create a simple test case to ensure non-standard library 'requests' works
response = requests.get('http://example.com')
print(f'Test case response status code: {response.status_code}')


# Existing code goes here...
# The rest of the file is the same as the provided ExecutePyFile.py script
