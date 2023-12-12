# /Agents/TeamMember.py

# Used to provide a definition to all agents
# Purpose is for each team member to acknowledge it is part of a work group and to be aware of who the other team members are

team_instruction = """
# Team Composition
You are not in this alone. You are part of an agency team of diverse roles each agent having their own speciality.
You are to acknolwedge your own strengths and to work (or in complex situations, refuse) any command or query that you know you are the best suited agent for.
You are to understand the services offered by others and to use your tool 'Delegate' to delegate a task to them because they are better suited than you.
"""

tool_instruction = """
# Shared Toolkit
The agency has a variety of tools at the disposal of all agents.
They are to be considered during planning and tool usage is expected to be the method of conducting operational task(s).
Tool are designed to be used by anyone, however consider whether a tool is relevant for a given missing. Ignore the ones that are not clear given your role.
"""

from Agents import UserAgent, CodingAgent, QaAgent, RecipeAgent
from Tools.ReadFile import ReadFile
from Tools.Plan import Plan
from Tools.Delegate import Delegate
from Tools.CreateFile import CreateFile
from Tools.MoveFile import MoveFile
from Tools.ExecutePyFile import ExecutePyFile

def get_team_instruction():
    # Build a generic team member instruction set that will be prepended to each agent's instructions
    
    # Make them aware of the agents available:
    team_member_instructions = team_instruction
    team_member_instructions += "\n## Agency\n"
    for agent in [UserAgent, CodingAgent, QaAgent, RecipeAgent]:
        team_member_instructions += "### " + agent.name + "\n" 
        team_member_instructions += agent.description + "\n"
        team_member_instructions += agent.services + "\n"
    team_member_instructions += "\n\n"
    
    # Make them aware of the tools available:
    team_member_instructions += tool_instruction
    team_member_instructions += "\n## Tools\n"
    for toolFile in [ReadFile, CreateFile, MoveFile, ExecutePyFile, Delegate, Plan]:
        schema = toolFile.openai_schema
        team_member_instructions += "### " + schema['name'] + "\n"
        team_member_instructions += schema['description'] + "\n\n"
    team_member_instructions += "\n\n"
    
    return team_member_instructions