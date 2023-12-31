# /Agents/TeamMember.py

# Used to provide a definition to all agents
# Purpose is for each team member to acknowledge it is part of a work group and to be aware of who the other team members are

from Agency.Arsenal import ORGANIZATIONAL, FILE_MANAGEMENT, PROGRAMMING, CUSTOM_TOOLS
    
class Team:
    
    TEAM_INSTRUCTION = """
    # Team Composition
    You are not in this alone. You are part of an agency team of diverse roles each agent having their own speciality.
    You are to acknolwedge your own strengths and to work (or in complex situations, refuse) any command or query that you know you are the best suited agent for.
    The agency does not work in parallel but rather a chain of handoffs. The agency has only one active agent at a time, the active agent being the one currently operating the mission.
    You are to understand the services offered by others and to use your tool 'Delegate' accordingly when a task is designated for a more specialized team member.
    The team is to always adhere the fulfillment of the user-approved agency's plan. Your own decisions are to respect the plan. Your own operations are to be conducted in accordance to the plan.
    The agency shares the same communication channel, so pay attention to previous events and who has conducted what so far.
    """.strip()

    TOOL_INSTRUCTION = """
    # Shared Toolkit
    The agency has a variety of tools at the disposal of all agents.
    They are to be considered during planning and tool usage is expected to be the method of conducting operational task(s). 
    When working the agency's plan, you are to always use your tools to complete your actionable steps. Once finished, use the 'Delegate' to the next agent in the plan.
    Tool are designed to be used by anyone, however consider whether a tool is relevant for a given mission. Ignore the ones that are not clear given your role.
    """.strip()

    @staticmethod
    def build_agents_list_and_arsenal():
        from Agents import agent_classes
        # Build a generic team member instruction set that will be prepended to each agent's instructions
        
        # Make them aware of the agents available:
        team_member_instructions = Team.TEAM_INSTRUCTION
        team_member_instructions += "\n\nThe Agency:\n"
        for agent in agent_classes.values():
            team_member_instructions += f"## {agent.NAME}:\n" 
            team_member_instructions += agent.DESCRIPTION + "\n"
            team_member_instructions += agent.SERVICES + "\n\n"
        
        # Make them aware of the tools available:
        team_member_instructions += Team.TOOL_INSTRUCTION
        
        team_member_instructions += "\n\n## Organizational Tools\n"
        for toolFile in ORGANIZATIONAL:
            schema = toolFile.openai_schema
            team_member_instructions += f"### {schema['name']}:\n{schema['description']}\n"
            
        team_member_instructions += "\n## File Management Tools\n"
        for toolFile in FILE_MANAGEMENT:
            schema = toolFile.openai_schema
            team_member_instructions += f"### {schema['name']}:\n{schema['description']}\n"
            
        team_member_instructions += "\n## Programming Tools\n"
        for toolFile in PROGRAMMING:
            schema = toolFile.openai_schema
            team_member_instructions += f"### {schema['name']}:\n{schema['description']}\n"
            
        team_member_instructions += "\n## Agent specific Tools\n"
        for toolFile in CUSTOM_TOOLS:
            schema = toolFile.openai_schema
            team_member_instructions += f"### {schema['name']}:\n{schema['description']}\n"
        
        return team_member_instructions