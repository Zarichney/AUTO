# bigoven selector module

selectors = {
    'base_url': 'https://www.bigoven.com',
    'search_page': '/recipes/',
    'listed_recipe': '.recipe-tile-full .panel-body > a[href*="/recipe/"]',
    'title': '.recipe-container h1',
    'description': '.about-recipe .summary',
    'image': 'recipe-upper-row img.recipe-hero-photo',
    'servings': '.yield',
    'prep_time': '',
    'cook_time': '',
    'total_time': '.ready-in',
    'ingredients': 'ul.ingredients-list li',
    'directions': '.recipe-instructions .instructions p',
    'notes': '.overview-notes',
}