from Agency.Agency import Agency
from Agents import CulinaryAgent
from Utilities.Log import Log, type

agency:Agency = Agency()

recipe_agent:CulinaryAgent = agency.get_agent(CulinaryAgent.NAME)
agency.active_agent = recipe_agent

# prompt = "Read the file 'meals.txt' and you'll find a list of meals\n"
# prompt += "Read the file 'recipe_template.md' and you'll find a markdown template file to make recipes with\n"
prompt = "I would like to make a cookbook from this list.\n\n"
prompt += "Phase one: Using your tool 'RecipeScraper', gather a list of recipes from the internet.\n"
prompt += "For the second phase, you will analyze the scraped recipes and sanitize the data."
prompt += "Then I want you to use your tool CreateFile to create a markdown file for each recipe, adhering to the template.\n"
prompt += "Use your tool GetDirectoryContents to review whether the files were created.\n"
prompt += "Keep using your tools until this mission is complete. Only respond once the full list from 'meals.txt' has been processed into a recipe markdown file for each meal in the list.\n"

# Phase one: gather recipes
agency.complete(
    mission_prompt=prompt, 
    single_agent=True,
    stop_word="continue", 
    continue_phrase="Move on to phase two"
)

# todo add custom session checkpoints:
# session.phase_one_complete = True
# agency.save_session(session)

prompt = "Phase two: Review the recipes and remove any scrapped recipes that are not relevant.\n"

# Phase two: clean recipe data
agency.complete(
    mission_prompt=prompt, 
    single_agent=True,
    stop_word="continue", 
    continue_phrase="Move on to phase three"
)

