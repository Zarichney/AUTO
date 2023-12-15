# bettycrocker selector module

selectors = {
    'base_url': 'https://www.bettycrocker.com/search?term=',
    'listed_recipe': '.searchNxResults li > div > a[href*="/recipes/"]',
    'title': '.recipeDetail h1',
    'description': '.recipeDescription',
    'image': '.rdpImage img',
    'servings': '.rdpAttributes ul li:nth-child(3) .attributeValue',
    'prep_time': '.rdpAttributes ul li:nth-child(1) .attributeValue',
    'cook_time': '',
    'total_time': '.rdpAttributes ul li:nth-child(2) .attributeValue',
    'ingredients': 'li.ingredient',
    'directions': 'li.recipeStep',
    'notes': '.nutritionPreview',
}