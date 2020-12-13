import random
from data.wine_categories import BOLD_WINES
from data.cheese_categories import STRONG_CHEESES, HARD_CHEESES, SOFT_CHEESES

def get_cheese_recommendation(wine, db):
    """
    This function serves as our rules engine for the app
    The function takes a wine JSON, chooses a cheese pairing, and returns a cheese JSON

    Most rules from: https://winefolly.com/wine-pairing/6-tips-on-pairing-wine-and-cheese/
    """

    query_obj = {}

    # Rule 1: Strong wines with strong cheeses
    if wine['abv'] > 14.5:
        strong = True
        query_obj['flavor'] = { '$in': STRONG_CHEESES }
    else:
        strong = False

    # Rule 2: Bold wines with aged cheeses (aged cheeses tend to be hard, blue, and stinky)
    if wine['grape'] in BOLD_WINES:
        bold = True
        query_obj['type'] = { '$in': HARD_CHEESES }
    else:
        bold = False

    # Rule 3: Sparkling wine with soft/creamy cheese
    if wine['Region'] == 'Champagne' or wine['name'].lower().find('sparkling') != -1:
        sparkling = True
        query_obj['texture'] = { '$in': SOFT_CHEESES }
    else:
        sparkling = False

    # Rule 4: Wines and cheeses from the same place pair well together
    region = wine['Country']
    if region == 'USA':
        region = 'United States'

    query_obj['location'] = region

    # Rule 5: Otherwise, get a firm, nutty cheese
    if not strong and not bold and not sparkling:
        query_obj['flavor'] = 'nutty'
        query_obj['type'] = 'firm'

    cheese_results = list(db.cheese.find(query_obj))

    # if our rules engine doesn't return any results, just pick a random cheese from the same region
    if len(cheese_results) < 1:
        cheese_results = list(db.cheese.find({ 'location': region }))

    return random.choice(cheese_results)