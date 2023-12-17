from Agents.Agent import Agent
from Agents.Agency import Agency
from Agents import RecipeAgent
from Utilities.Log import Log, colors

agency:Agency = Agency(prompt="Lets create some recipes", new_session=True, build_agents=True)

recipe_agent:Agent = agency.get_agent(RecipeAgent.name)

prompt = "Read the file 'meals.txt' and you'll find a list of meals\n"
prompt += "Read the file 'recipe_template.md' and you'll find a markdown template file to make recipes with\n"
prompt += "I would like to make a cookbook from this list.\n"
prompt += "For each meal, use your tool RecipeScraper to gather a list of recipes from the internet.\n"
prompt += "Consider each recipe that is scrapped, as not all recipes are exact matches for what the scraper tool is capable of searching. You are to use your knowledge to filter out or ignore any irrelevant recipes.\n"
prompt += "Then I want you to use your tool CreateFile to create a markdown file for each recipe, adhering to the template.\n"
prompt += "The new recipe is to be inspired by existing recipes. However when the scrapped recipes are not exact matches, you are to use your knowledge to fill in the gaps.\n"
prompt += "You may use your tool GetDirectoryContents to review whether all recipes have been written to markdown files.\n"
prompt += "Keep using your tools until this mission is complete. Only respond once the full list from 'meals.txt' has been processed into a recipe markdown file for each meal in the list.\n"

Log(colors.COMMUNICATION, f"User: {prompt}")

while True:

    response = recipe_agent.get_completion(message=prompt)

    Log(colors.RESULT, f"{recipe_agent.name}:\n{response}")

    prompt = input("Waiting for reply from user. Type 'exit' to terminate\n\n> ")

    if prompt.lower() == "exit":
        Log(colors.ACTION, "Exiting...")
        break
