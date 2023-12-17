# bbcfood selector module

# CSS selectors for scraping the data
selectors = {
    'base_url': 'https://www.bbc.co.uk',
    'search_page': '/food/search?q=',
    'listed_recipe': '.search-page__promo-collection a[href*="/food/recipes/"]',
    'title': 'h1.content-title__text',
    'description': '.recipe-description__text',
    'image': '.recipe-media__image img',
    'servings': '.recipe-metadata__serving',
    'prep_time': '.recipe-metadata__prep-time',
    'cook_time': '.recipe-metadata__cook-time',
    'total_time': '',
    'ingredients': '.recipe-ingredients__list li',
    'directions': '.recipe-method__list li',
    'notes': '.recipe-ingredients__sub-heading',
}