# inspiretraveleat selector module

selectors = {
    'base_url': "https://www.inspiretraveleat.com",
    'search_page': '/?s=',
    'listed_recipe': 'article h2 a',
    'title': '.fl-heading',
    'description': '.fl-module-fl-post-content p:nth-child(2)',
    'image': '.wprm-recipe-image img',
    'prep_time': '.wprm-recipe-time-container:nth-child(1) .wprm-recipe-time',
    'cook_time': '.wprm-recipe-time-container:nth-child(2) .wprm-recipe-time',
    'total_time': '.wprm-recipe-time-container:nth-child(3) .wprm-recipe-time',
    'servings': '.wprm-recipe-servings-with-unit',
    'ingredients': '.wprm-recipe-ingredients-container li',
    'directions': 'li.wprm-recipe-instructio',
    'notes': '',
}