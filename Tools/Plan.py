# /Tools/Plan.py

from instructor import OpenAISchema
from pydantic import Field
from Utilities.Log import Log, Debug, colors
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Agents.Agent import Agent
    from Agents.Agency import Agency

class Plan(OpenAISchema):
    """
    Used to review mission against the environment (team and/or tools resources available) to generate a workflow of action items.
    """

    mission: str = Field(
        ..., 
        description="The goal that the agent would like to achieve. Will be used as the basis for planning"
    )

    team_planning: bool = Field(
        default=False,
        description="Flag to indicate whether the plan is for the entire team or just the agent. If true, the plan will include the team composition."
    )

    def run(self, agency: 'Agency'):
            
        current_agent = agency.active_agent

        master_plan_creation = agency.plan is None

        prompt = "You are being engaged to create a plan. Review the following:\n\n"
        prompt += "User's Prompt: " + agency.prompt + "\n\n"
        if master_plan_creation == False:
            prompt += "Your mission is to: " + self.mission + "\n\n"

            prompt += "# Agency's Plan\n\n"
            prompt += agency.plan + "\n\n"

        if master_plan_creation or self.team_planning:
            # Add team details
            prompt += "# Team Composition: \n"
            for agent in agency.agents:
                agent:Agent = agent
                prompt += f"## Name: \"{agent.name}\"\n"
                prompt += f"### Description: {agent.description}\n"
                # prompt += f"### Services: {agent.services}\n" # TODO: fix: empty array []
                prompt += "\n"
            prompt += "\n"
        
        # Add available tools to prompt:
        if master_plan_creation or self.team_planning:
            toolkit = current_agent.shared_tools + current_agent.internal_tools
        else:
            toolkit = current_agent.tools
        
        prompt += "# Available Tools: \n"
        try:
            for tool in toolkit:
                schema = tool.openai_schema
                prompt += "## " + schema['name'] + "\n"
                prompt += schema['description'] + "\n\n"
            prompt += "\n"
        except Exception as e:
            Log(colors.ERROR, f"Error in Plan.py: {e}")
            Log(colors.ERROR, f"Toolkit: {toolkit}")
            Log(colors.ERROR, f"master_plan_creation: {master_plan_creation}")
            Log(colors.ERROR, f"self.team_planning: {self.team_planning}")
    
        # Instruction to review inputs and make a plan
        prompt += "# Plan Structure\n\n"
        prompt += "The plan is a workflow of actionable steps that will be executed to accomplish the mission.\n"
        prompt += "An Actional Step is specific instruction conducted by a single agent as either a single response or a tool usage\n"
        prompt += "Delegation is considered an actional step: it's the usage of the 'Delegate' tool.\n\n"
        prompt += "The plan format adhere's to the following structure:\n"
        prompt += "<step_number> + \". '\" + <agent_name> + \"'\" + (optional: \"-->'\" + <tool_name> + \"') + \": \" + <response | tool_usage>\"\n"
        prompt += "\nMulti Step Example:\n"
        prompt += "\t\"1. Coder: Create the script using tool 'CreateFile'\"\n"
        prompt += "\t\"2. Coder: Provide QA with the generated script to do a code review using tool 'Delegate'\"\n"
        prompt += "\t\"3. QA: Analyze script and provide feedback using tool 'ReadFile'\"\n"
        prompt += "\nSample of a simple one liner plan:\n"
        prompt += "\t\"1. User Agent: I will respond to the user's prompt\"\n\n"
        
        # Plan tweaking
        prompt += "## Additional considerations:\n"
        prompt += "- Ensure the plan is manageable:\n"
        prompt += "  - Recognize and acknowledge if the mission is too complex.\n"
        prompt += "    - Size complexity will depend on the context so use your judgement.\n"
        prompt += "    - It is acceptable that the user's prompt is as simple as a one step plan\n"
        prompt += "  - Refuse plan generation when:\n"
        prompt += "    - The mission is too general and cannot be executed via actionable steps.\n"
        prompt += "    - The execution to achieve the desired result is deemed infeasible.\n"
        prompt += "    - The request falls outside the agent's capabilities.\n"
        prompt += "    - During refusals, provide detailed explanations:\n"
        prompt += "      - Why the mission cannot be carried out or the plan cannot be generated.\n"
        prompt += "      - Clarify what changes are needed for a successful attempt.\n"
        prompt += "- Delegation is key:\n"
        prompt += "  - Each agent is equipped with 'Delegate' to perform the handoff of the tasks.\n"
        prompt += "  - The invocation of the tool 'Delegate' is to be it's own step in the plan, ensuring proper delegation.\n"

        prompt += "\n\n**THE GOAL IN PLAN CREATION IS TO SIMPLY CONSIDER THE MISSION AGAINST "
        if master_plan_creation or self.team_planning:
            prompt += "THE ENVIRONMENT (AGENTS AND TOOLS AVAILABLE)"
        else:
            prompt += "YOUR CAPABILITIES"
        prompt += " WITH THE LEAST AMOUNT OF ACTIONABLE STEPS NECESSARY**\n\n"
        prompt += "Think step by step. Good luck, you are great at this!\n"
            
        Debug(f"Plan Prompt for {current_agent.name}:\n{prompt}")
        
        if master_plan_creation:
            Log(colors.ACTION, f"Agency is generating a plan\n")
        
        plan = current_agent.get_completion(message=prompt, useTools=False)

        Log(colors.RESULT, f"\nPlan Generated:\n{plan}\n")
        
        return plan
        
