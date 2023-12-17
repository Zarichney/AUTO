# eatingwell selector module

selectors = {
    'base_url': "https://www.eatingwell.com",
    'search_page': '/search?q=',
    'listed_recipe': '.search-results a[href*="/recipe/"]',
    'title': '.article-heading',
    'description': '.article-subheading',
    'image': '.primary-image img',
    'prep_time': '.recipe-details .mntl-recipe-details__item:nth-child(1) .mntl-recipe-details__value',
    'cook_time': '.recipe-details .mntl-recipe-details__item:nth-child(2) .mntl-recipe-details__value',
    'total_time': '.recipe-details .mntl-recipe-details__item:nth-child(3) .mntl-recipe-details__value',
    'servings': '.recipe-details .mntl-recipe-details__item:nth-child(4) .mntl-recipe-details__value',
    'ingredients': '.mntl-structured-ingredients__list li',
    'directions': '.recipe__steps li',
    'notes': '',
}