# bbcgfood selector module

selectors = {
    'base_url': 'https://www.bbcgoodfood.com',
    'search_page': '/search?q=',
    'listed_recipe': 'article a[href*="/recipes/"]',
    'title': '.recipe h1',
    'description': '.recipe .editor-content',
    'image': '.recipe picture img',
    'servings': '.recipe .post-header__body ul li:nth-child(3)',
    'prep_time': '.recipe .post-header__body ul li:nth-child(1) ul li:nth-child(1)',
    'cook_time': '.recipe .post-header__body ul li:nth-child(1) ul li:nth-child(2)',
    'total_time': '',
    'ingredients': '.recipe__ingredients ul li',
    'directions': '.recipe__method-steps ul li',
    'notes': '',
}