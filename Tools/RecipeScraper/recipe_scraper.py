import json
import os
import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
from requests.exceptions import ConnectionError, HTTPError, Timeout
from sites import allrecipes, eatingwell, nytimes, bbcfood, bbcgoodfood, bettycrocker, bigoven, inspiretraveleat, wordpress, iowagirleats

MAX_NUM_RECIPES_PER_SITE = 3
OUTPUT_DIRECTORY_NAME = "Recipes"

SITE_SELECTORS = {
    'allrecipes': allrecipes.selectors,
    'eatingwell': eatingwell.selectors,
    'nytimes': nytimes.selectors,
    'bbcfood': bbcfood.selectors,
    'bbcgoodfood': bbcgoodfood.selectors,
    'bettycrocker': bettycrocker.selectors,
    'bigoven': bigoven.selectors,
    'inspiretraveleat': inspiretraveleat.selectors,
    'kaleforniakravings': wordpress.selectors,
    "4sonrus": wordpress.selectors,
    "kitchenconfidante": wordpress.selectors,
    "simplykitch": wordpress.selectors,
    "iowagirleats": iowagirleats.selectors,
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
        print(f"Error occurred during request_get: {e}")
    return None

def extract_text(parser, selector, attribute=None):
    if not selector:
        return None
    
    try:
        element = parser.select_one(selector)
        if element is not None:
            if attribute:
                return element.get(attribute)
            else:
                return element.get_text(strip=True)
            
    except Exception as e:
        print(f"Error occurred with selector {selector} during extract_text: {e}")
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
        
        recipe['title'] = extract_text(parser, selectors['title'])
        recipe['description'] = extract_text(parser, selectors['description'])
        recipe['image_url'] = extract_text(parser, selectors['image'], 'data-lazy-src')
        if not recipe['image_url']:
            recipe['image_url'] = extract_text(parser, selectors['image'], 'src')
        recipe['servings'] = extract_text(parser, selectors['servings'])
        recipe['prep_time'] = extract_text(parser, selectors['prep_time'])
        recipe['cook_time'] = extract_text(parser, selectors['cook_time'])
        recipe['total_time'] = extract_text(parser, selectors['total_time'])
        recipe['ingredients'] = [li.get_text(strip=True) for li in parser.select(selectors['ingredients'])]
        recipe['directions'] = [step.get_text(strip=True) for step in parser.select(selectors['directions'])]
        recipe['notes'] = extract_text(parser, selectors['notes'])

    except Exception as e:
        print(f"Error occurred during parse_recipe: {e}")
        return None

    return recipe

def scrape_recipes(site, food_item):
    
    selectors = SITE_SELECTORS[site]
    site_url = selectors['base_url']
    
    # wordpress sites dont have the base_url set, build it using the site
    if not site_url:
        site_url = f"https://{site}.com"
    
    search_url = f'{site_url}{selectors["search_page"]}{quote_plus(food_item)}'
    response = request_get(search_url)
    if not response:
        return None
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Get list of urls from the search result page
    selector = selectors['listed_recipe']
    links = soup.select(selector)
    urls = [link['href'] for link in links]
    
    if not urls:
        print(f"No recipes found for {food_item} on {site_url}")
        return None
    
    # remove any duplicate hrefs
    urls = list(dict.fromkeys(urls))
    
    recipes = []

    # Iterate through search results to extract from each recipe url
    for url in urls:
        
        # Append domain when url is relative
        if not url.startswith('https://'):
            url = f"{site_url}{url}"

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

    all_recipes = []
    
    for site in SITE_SELECTORS:

        if not SITE_SELECTORS[site]['search_page']:
            print(f"site missing the search page url")
            continue
        
        recipes = scrape_recipes(site, food_item)
        if recipes is not None and len(recipes) > 0:
            all_recipes.extend(recipes)
            
    if all_recipes and len(all_recipes) > 0:
        save_to_json(food_item, all_recipes)
        print(f"Successfully saved {len(all_recipes)} recipes for {food_item}.")
    else:
        print("Failed to retrieve data for any recipes.")