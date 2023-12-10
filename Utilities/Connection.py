# /Utilities/Connection.py

def GetKey():
    with open('openai.key', 'r') as file:
        return file.read().strip()