healthyIngredientsMap = {'sugar': 'stevia', 'salt': 'sea-salt', 'whole milk': 'reduced fat milk', 'butter': 'olive oil',
                         'mayo': 'sour cream', 'mayonnaise': 'sour cream', 'bacon': 'turkey bacon',
                         'all-purpose flour': 'whole wheat flour', 'ground beef': 'extra lean ground beef',
                         'dressing': 'vinegar', 'palm oil': 'olive oil', 'coconut oil': 'olive oil',
                         'vegetable oil': 'olive oil', 'bread crumbs': 'ground flaxseeds', 'white rice': 'brown rice',
                         'pasta': 'whole wheat pasta', 'kosher salt': 'sea-salt', 'spaghetti': 'whole wheat pasta'}

cookingTools = ['pan', 'grater', 'whisk', 'tong', 'spatula', 'knife', 'oven', 'microwave', 'skillet', 'saucepan', 'pot',
                'bowl', 'plate', 'baking sheet', 'stovetop']

frenchToIndian = {'cheese': 'paneer', 'leeks': 'onions', 'shallots': 'garlic', 'tarragon': 'cardamom',
                  'herbes de provence': 'garam masala', 'butter': 'mustard oil', 'olive oil': 'mustard oil',
                  'fleur de sel': 'coriander', 'duck': 'chicken', 'bread': 'naan', 'baguette': 'naan',
                  'mustard': 'curry'}

italianToChinese = {'pasta': 'lo mein noodles', 'spaghetti': 'lo mein noodles',
                    'cheese': 'tofu', 'Alfredo': 'soy sauce', 'macaroni': 'lo mein noodles',
                    'green bell pepper': 'bok choy', 'italian': 'chinese', 'bread': 'rice',
                    'olive oil': 'vegetable oil', 'tomato sauce': 'soy sauce',
                    'tomato': 'dried chilli peppers', 'lasagna': 'lo mein', 'parsley': 'ginger', 'bread crumbs': 'rice'}

chineseToItalian = {'rice': 'pasta', 'vegetable oil': 'olive oil', 'soy sauce': 'tomato sauce',
                    'sesame oil': 'olive oil',
                    'ginger': 'parsley', 'bok choy': 'green bell pepper', 'hot chile paste': 'tomato sauce',
                    'chinese': 'italian',
                    'hoisin': 'tomato sauce', 'five-spice powder': 'black pepper', 'rice vinegar': 'olive oil',
                    'oyster': 'tomato sauce', 'asian': 'italian'}

americanToMiddleEastern = {'bacon': 'lamb bacon', 'pork': 'lamb', 'ham': 'lamb ham',
                           'bacon grease': 'olive oil', 'canola oil': 'olive oil', 'vegetable oil': 'olive oil',
                           'American cheese': 'feta cheese', 'cheddar': 'feta', 'blue cheese': 'feta cheese',
                           'cheese curd': 'feta', 'colby': 'feta', 'colby-jack': 'labneh', 'cream cheese': 'halloumi',
                           'monterey jack': 'ackawi', 'pepper jack cheese': 'nabulsi',
                           'string cheese': 'jibneh arabieh',
                           'parmesan': 'testouri', 'swiss cheese': 'shanklish', 'nacho cheese': 'hummus',
                           'pink bean': 'chickpea', 'pinquito': 'chickpea', 'ketchup': 'tomato', 'mustard': 'sumac',
                           'paprika': 'cumin', 'oregano': 'parsley', 'tortilla': 'pita', 'yogurt': 'greek yogurt',
                           'mayonnaise': 'tahini', 'jalapeno pepper': 'peppercorn', 'navy bean': 'chickpea',
                           'molasse': 'honey', 'syrup': 'honey', 'mustard': 'cumin', 'worcestershire sause': 'tahini',
                           'brown sugar': 'honey', 'powdered sugar': 'honey', 'granulated sugar': 'honey',
                           'hot sauce': 'tahini', 'hot pepper sauce': 'tahini', 'bratwurst': 'lamb sausage',
                           'grits': 'rice', 'white sugar': 'honey', 'cornmeal': 'chickpea flour',
                           'oatmeal': 'rice', 'bread': 'pita bread', 'squash': 'cucumber', 'zucchini': 'cucumber',
                           'pickle': 'olive', 'bell pepper': 'cucumber', 'shrimp': 'beef', 'whipping cream': 'honey',
                           'whipped cream': 'honey', 'heavy cream': 'whole milk', 'green onion': 'coriander',
                           'corn flour': 'wheat flour', 'cornmeal': 'rice', 'chocolate chips': 'mixed nuts',
                           'hamburger bun': 'pita bread', 'hotdog bun': 'pita bread', 'sour cream': 'coconut cream',
                           'celery': 'okra', 'crackers': 'pita chips', 'maple syrup': 'honey',
                           'soy sauce': 'sesame oil',
                           'coleslaw mix': 'cucumber tomato mix', 'salad dressing': 'sesami oil',
                           'poppy seeds': 'cumin',
                           'half-and-half': 'goatmilk', 'sweet potato': 'carrot', 'pie crust': 'baklava crust',
                           'cooking sherry': 'nutmeg', 'linguine pasta': 'couscous', 'spaghetti': 'couscous',
                           'cookie dough': 'phyllo dough', 'basil': 'thyme', 'asparagus': 'okra',
                           'balsamic vinegar': 'sumac',
                           'andoille sausage': 'lamb sausage', 'cilantro': 'coriander', 'salsa': 'hummus',
                           'bay leaves': 'cinnamon', 'kidney bean': 'black bean', 'garbanzo bean': 'chickpea',
                           'bread dough': 'phyllo dough', 'italian sausage': 'beef kebab', 'fennel seed': 'cinnamon',
                           'oats': 'mujadara pilaf', 'steak': 'shish kabob', 'pizza dough': 'pita bread dough',
                           'house salad': 'tabouli salad', 'salsa dip': 'tabouli salad',
                           'ricotta cheese': 'feta cheese',
                           'enchilada sauce': 'hummus'}

mexicanToSoulFood = {'avocado': 'sweet potato', 'beans': 'black eyed peas', 'salsa': 'gravy',
                     'hot sauce': 'barbecue sauce', 'chili pepper': 'cayenne pepper', 'maize': 'corn',
                     'tortilla': 'cornbread',
                     'rice': 'grits', 'chicken': 'pork', 'lettuce': 'collard greens', 'chorizo': 'sausage',
                     'tequila': 'bourbon', 'crema': 'sour cream', 'tomatillo': 'tomato', 'nopales': 'okra',
                     'poblanos': 'cayenne peppers', 'chipotle': 'cayenne pepper', 'steak': 'brisket',
                     'carne asada': 'chicken fried steak',
                     'guacamole': 'gravy', 'shrimp': 'crawfish', 'crab': 'crawfish', 'squash': 'sweet potato',
                     'cabbage': 'collard greens'}
