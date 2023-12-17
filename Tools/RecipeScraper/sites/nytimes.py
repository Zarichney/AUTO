# nytimes selector module

selectors = {
    'base_url': 'https://cooking.nytimes.com',
    'search_page': '/search?q=',
    'listed_recipe': 'ul[class*="cardgrid"] a[href*="/recipes/"]',
    'title': '.recipe h1',
    'description': '.recipe .pantry--body',
    'image': '.recipe [class*="recipeheaderimage"] img',
    'servings': '.recipe [class*="recipeYield"]',
    'prep_time': '.recipe [class*="cookingTime"] :nth-child(4)',
    'cook_time': '.recipe [class*="cookingTime"] :nth-child(6)',
    'total_time': '.recipe [class*="cookingTime"] :nth-child(2)',
    'ingredients': '.recipe [class^="recipebody_ingredients"] ul li',
    'directions': '.recipe [class^="recipebody_prep"] ol li',
    'notes': '.recipe [class^="recipebody_prep"] [class^="tips"]',
}