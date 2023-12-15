import json
import os
import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
from requests.exceptions import ConnectionError, HTTPError, Timeout
from sites import allrecipes, eatingwell, nytimes, bbcfood, bbcgoodfood, bettycrocker, bigoven

MAX_NUM_RECIPES_PER_SITE = 5
OUTPUT_DIRECTORY_NAME = "Recipes"

SITE_SELECTORS = {
    'allrecipes': allrecipes.selectors,
    'eatingwell': eatingwell.selectors,
    'nytimes': nytimes.selectors,
    'bbcfood': bbcfood.selectors,
    'bbcgoodfood': bbcgoodfood.selectors,
    'bettycrocker': bettycrocker.selectors,
    'bigoven': bigoven.selectors,
}

# JSON format for storing the recipe data
recipe_structure = {
    "recipe_url": '',
    "title": '',
    "description": '',
    "image_url": '',
    "servings": '',
    "prep_time": '',
    "cook_time": '',
    "total_time": '',
    "ingredients": [],
    "directions": [],
    "notes": '',
}

ALLOW_REDIRECTS = False
TIMEOUT = 10  # seconds
HEADERS = {
    "Accept-Encoding": "gzip, deflate, sdch",
    "Accept-Language": "en-US,en;q=0.8",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
}

def request_get(url):
    try:
        print(f"Running requests.get for url: {url}")
        response = requests.get(
            url=url, allow_redirects=ALLOW_REDIRECTS, headers=HEADERS, timeout=TIMEOUT
        )
        response.raise_for_status()
        return response
    except HTTPError as e:
        print(f"HTTP error occurred: {e}")
    except ConnectionError as e:
        print(f"Network problem: {e}")
    except Timeout as e:
        print(f"Timeout occurred: {e}")
    except Exception as e:
        print(f"Error occurred: {e}")
    return None

# Function to parse a recipe page and extract information
def parse_recipe(url, selectors):
    
    response = request_get(url)
    if not response:
        return None

    recipe = dict(recipe_structure)
    parser = BeautifulSoup(response.text, "html.parser")

    try:
        recipe['recipe_url'] = url

        if selectors['title']:
            recipe['title'] = parser.select_one(selectors['title']).get('src', '')

        if selectors['description']:
            recipe['description'] = parser.select_one(selectors['description']).get('src', '')

        if selectors['image']:
            recipe['image_url'] = parser.select_one(selectors['image']).get('src', '')

        if selectors['servings']:
            recipe['servings'] = parser.select_one(selectors['servings']).get_text(strip=True)

        if selectors['total_time']:
            recipe['total_time'] = parser.select_one(selectors['total_time']).get_text(strip=True)

        if selectors['prep_time']:
            recipe['prep_time'] = parser.select_one(selectors['prep_time']).get_text(strip=True)

        if selectors['cook_time']:
            recipe['cook_time'] = parser.select_one(selectors['cook_time']).get_text(strip=True)

        recipe['ingredients'] = [li.get_text(strip=True) for li in parser.select(selectors['ingredients'])]

        recipe['directions'] = [step.get_text(strip=True) for step in parser.select(selectors['directions'])]

        if selectors['notes']:
            recipe['notes'] = parser.select_one(selectors['notes']).get_text(strip=True)

    except Exception as e:
        print(f"Error occurred: {e}")
        return None

    return recipe

def scrape_recipes(food_item, selectors):
    
    search_url = f'{selectors["base_url"]}{quote_plus(food_item)}'
    response = request_get(search_url)
    if not response:
        return None
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Get list of urls from the search result page
    links = soup.select(selectors['listed_recipe'])
    urls = [link['href'] for link in links if 'http' in link['href']]
    
    recipes = []

    # Iterate through search results to extract from each recipe url
    for url in urls:

        recipe = parse_recipe(url, selectors)
        if recipe:
            recipes.append(recipe)

        if len(recipes) == MAX_NUM_RECIPES_PER_SITE:
            # Stop iterating search matched recipes
            break
            
    return recipes

# Function to save data into a JSON file
def save_to_json(filename, data):

    # if doesnt exist, create recipe output directory
    if not os.path.exists(OUTPUT_DIRECTORY_NAME):
        os.makedirs(OUTPUT_DIRECTORY_NAME)

    with open(f"{OUTPUT_DIRECTORY_NAME}/{filename}.json", "w") as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    # if no arguments have been supplied, then return
    if len(sys.argv) == 1:
        print(
            "No arguments supplied, please provide a food item such as 'Onion Soup Burger'"
        )
        sys.exit()

    food_item = sys.argv[1]
    # food_item = "Onion Soup Burger"

    all_recipes = []
    
    for site in SITE_SELECTORS:

        if not SITE_SELECTORS[site]['base_url']:
            print(f"site missing the search page url")
            continue

        recipes = scrape_recipes(food_item, SITE_SELECTORS[site])
        if len(recipes) > 0:
            all_recipes.extend(recipes)
        else:
            print(f"Failed to retrieve recipes from site {site}.")
            
    if all_recipes and len(all_recipes) > 0:
        save_to_json(food_item, all_recipes)
        print(f"Successfully saved {len(all_recipes)} recipes for {food_item}.")
    else:
        print("Failed to retrieve data for any recipes.")