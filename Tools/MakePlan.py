# /Tools/MakePlan.py

from typing import Dict
from instructor import OpenAISchema
from pydantic import Field
from Utilities.Log import Log, colors
from Agents.Agent import Agent
from Utilities.OpenAiHelper import GetCompletion
from Utilities.Helpers import GetAgent
from Tools.ReadFile import ReadFile
from Tools.ExecutePyFile import ExecutePyFile
from Tools.RequestAssistance import RequestAssistance
from Tools.CreateFile import CreateFile
from Tools.MoveFile import MoveFile

class MakePlan(OpenAISchema):
    """
    Used to review the command or query against the environment (team and tools resources available) to generate a plan of action items
    """

    caller_name: str = Field(..., description="The name of the assistant that invoked this tool")

    prompt: str = Field(..., description="The prompt that the agent received. Will be used as the basis for planning")

    def run(self, agency: Dict[str, Agent], client):
        prompt = "You are being engaged to create a plan. First review the following:\n\n"
        prompt += "Prompt: " + self.prompt + "\n"
        
        # Add team details
        prompt += "Team: \n"
        for agent_key in agency:
            agent: Agent = agency[agent_key]
            prompt += f"- Name: \"{agent.name}\"\n"
            prompt += f"  - Description: {agent.description}\n"
            prompt += f"  - Services: {agent.services}\n"
        prompt += "\n\n"
            
        current_agent = GetAgent(client, agency, self.caller_name)
        
        # Add available tools to prompt:
        prompt += "Available Tools: \n"
        prompt += f"- RequestAssistance: {RequestAssistance.openai_schema}\n" 
        prompt += f"- ReadFile: {ReadFile.openai_schema}\n"
        prompt += f"- MoveFile: {MoveFile.openai_schema}\n"
        prompt += f"- CreateFile: {CreateFile.openai_schema}\n"
        prompt += f"- ExecutePyFile: {ExecutePyFile.openai_schema}\n"
    
        # Instruction to review inputs and make a plan
        prompt += "\nNow, with an understanding the goal, analyze the team's dynamics along with knowing what tools they have at their disposal,"
        prompt += "\n\t\tGENERATE A PLAN\t\t\n\n"
        prompt += "The plan is a workflow of 1-12 actionable steps that will be executed to accomplish the mission.\n"
        prompt += "An Actional Step is defined as a single response (command or query) or tool usage that is conducted by a single agent.\n"
        prompt += "Delegation is considered an actional step: it's the usage of the 'RequestAssistance' tool.\n\n"
        prompt += "The plan format adhere's to the following structure:\n"
        prompt += "<step_number>. <agent_name>: <command, query or tool>\n"
        prompt += "\nExample: \"1. Coder: Create the script\"\n\n"
        
        # Plan tweaking
        prompt += "Additional considerations:\n"
        prompt += "- Ensure the plan is manageable:\n"
        prompt += "  - Recognize and acknowledge if the mission is too complex.\n"
        prompt += "  - Refuse plan generation when:\n"
        prompt += "    - The mission is too general and cannot be executed via actionable steps.\n"
        prompt += "    - The desired result is deemed infeasible.\n"
        prompt += "    - The request falls outside the agent's capabilities.\n"
        prompt += "  - During refusals, provide detailed explanations:\n"
        prompt += "    - Why the mission cannot be carried out or the plan cannot be generated.\n"
        prompt += "    - Clarify what changes are needed for a successful attempt.\n"
        prompt += "- Delegation is key:\n"
        prompt += "  - Each agent is equipped with 'RequestAssistance' to perform the handoff of the tasks.\n"
        prompt += "  - The invocation of the tool 'RequestAssistance' is to be it's own step in the plan, ensuring proper delegation.\n"
        prompt += "- Size complexity will depend on the context so use your judgement.\n"
        prompt += "  - A good rule of thumb is that a resonably complex plan involves more than 8 actionable steps.\n"
        prompt += "  - It is also acceptable that the prompt (command or query) is as simple as a one step plan"
        
        prompt += "\n\nThink step by step. Good luck, you are great a this!\n"
            
        Log(colors.ACTION, f"{current_agent.name} is planning...")

        plan = GetCompletion(client=client, message=prompt, agent=current_agent, useTools=False)
        
        plan += "\nNext what needs to be done is to use my tools to accomplish step one, or use the tool 'RequestAssistance' to request help from another agent.\n"

        Log(colors.COMMUNICATION, f"\nPlan Generated:\n{plan}\n")
        
        return plan
        