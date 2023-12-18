# /Tools/RecipeScraper/RecipeScaper.py

import json
import os
import subprocess
import sys
from instructor import OpenAISchema
from pydantic import Field
from Utilities.Log import Debug, Log, type

class RecipeScaper(OpenAISchema):
    """
    Scrapes the internet for a collection of a given recipe. Returns JSON of recipes.
    """

    meal: str = Field(
        ...,
        description="The name of the recipe to search the internet for"
    )

    def run(self):

        directory = "./Tools/RecipeScraper/"
        script = "recipe_scraper.py"
        if not os.path.exists(self.directory + script):
            Log(type.ERROR, f"Unexpected script location: {directory + script}")

        # Get the path of the current Python interpreter
        python_path = sys.executable

        Log(type.ACTION, f"Executing recipe scraper for: {self.meal}")
        Debug(f"Agent called subprocess.run with:\n{[python_path, directory + script] + self.meal}")
        
        try:
            execution = subprocess.run(
                [python_path, directory + script] + self.meal,
                text=True,
                capture_output=True,
                check=True,
                timeout=10
            )
            Debug(f"{script} execution result: {execution.stdout}")

            recipes = []

            # Output is expected to be a json file under the directory 'Recipes' as an array of recipes
            Debug(f"Reading json result")
            with open(f"{directory}/Recipes/{self.meal}.json", "r") as f:
                result = json.load(f)
                
            recipes = result

            if not recipes:
                result = f"No recipes were able to be scraped..."
                Log(type.RESULT, result)
                return result
            
            Log(type.RESULT, f"Analyzing {len(recipes)} recipes")

            # Return to agent the json as string
            return json.dumps(recipes)

        except subprocess.TimeoutExpired:
            result = "Execution timed out. The script may have been waiting with a prompt."
            Log(type.ERROR, result)
            return result

        except subprocess.CalledProcessError as e:
            result = f"Execution error occurred: {e.stderr}"
            Log(type.ERROR, result)
            return result
            