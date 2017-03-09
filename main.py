import requests, bs4, sys, ingredient, protein, foodList


def find_sub_list(sl,l):
    results=[]
    sll=len(sl)
    for ind in (i for i,e in enumerate(l) if e==sl[0]):
        if l[ind:ind+sll]==sl:
            results.append((ind,ind+sll-1))

    return results

if len(sys.argv) != 3:
    print "usage: python main.py [url of recipe in single quotes] [transformation]"
    quit()

args = sys.argv

recipeUrl = args[1]
transformation = args[2]

# get webpage
res = requests.get(recipeUrl)
res.raise_for_status()
recipe = bs4.BeautifulSoup(res.text,"html.parser")

# get the title
title = []
for word in recipe.findAll("h1", {"class" : "recipe-summary__h1"}):
    title.append(word.get_text())
    # print word.get_text()
# print title

# get ingredients --->>> there's extra stuff on the end we don't want
ingredients = []
for word in recipe.findAll("span", { "class" : "recipe-ingred_txt" }):
    ingredients.append(word.get_text())
    # print word.get_text()
ingredients = [x for x in ingredients if x != "Add all ingredients to list" and x != ""]
# print ingredients

# get prep time
prepTime = []
for word in recipe.findAll("time", { "itemprop" : "prepTime" }):
    prepTime.append(word.get_text())
    # print word.get_text()
# print prepTime

# get cook time
cookTime = []
for word in recipe.findAll("time", { "itemprop" : "cookTime" }):
    cookTime.append(word.get_text())
    # print word.get_text()
# print cookTime

# get total time
totalTime = []
for word in recipe.findAll("time", { "itemprop" : "totalTime" }):
    totalTime.append(word.get_text())
    # print word.get_text()
# print totalTime

# get directions
directions = []
for word in recipe.findAll("span", { "class" : "recipe-directions__list--item" }):
    directions.append(word.get_text())
    # print word.get_text()
# directions = [each.split('.') for each in directions]
# print directions
# print directions

# get footnotes
# footnotes = []
# for word in recipe.findAll("section", {"class" : "recipe-footnotes"})[0].findAll("li"):
#     footnotes.append(word.get_text())
    # print word.get_text()
# print footnotes

###################
# parse ingredients
###################

fractions = ['1/2', '1/3', '1/4', '1/8', '1/16', '2/3', '3/4', '3/8', '5/8', '7/8']

numbers = [str(x) for x in range(0, 100)]

decNumbers = []
for num in numbers:
    decNumbers.append(num + '.25')
    decNumbers.append(num + '.5')
    decNumbers.append(num + '.75')
numbers += decNumbers

measurements = ['teaspoon', 'tsp', 'tablespoon', 'tbsp', 'cup', 'pound', 'lbs', 'dash', 'pinch', 'scoop',
                'ounce', 'oz', 'fl', 'oz', 'fluid', 'ounce', 'fluid', 'oz', 'pint', 'pt.', 'quart', 'qt.',
                'gallon', 'gal.', 'ml', 'milliliter', 'l', 'liter', 'gram', 'g', 'kilogram', 'kg', 'stick', 'T',
                'large', 'small', 'medium', 'regular', 'clove']

pluralMeasurements = []
for measurement in measurements:
    pluralMeasurements.append(measurement + 's')
    pluralMeasurements.append(measurement + 'es')
measurements += pluralMeasurements

descriptors = ['fresh', 'extra', 'virgin', 'extra-virgin','white']

sup_methods = ['chop','grate','stir', 'shake', 'mince', 'crush', 'squeeze','sprinkle','season','dissolve','peel',
               'seed','mix','grind','ground','dry','cure','grease','degrease','dredge','dehydrate','dried','brush',
               'fold','cut','stuff','ferment','flambe','foam','can','paste','steep','infuse','dissolve','juice',
               'marinate','soak','pasteurize','pickle','puree','pure','reduce','reduction','separate','shir',
               'smother','sous-vide','thicken','devein','glaze','frozen','chill','mash']

variations = []
for each in sup_methods:
    variations.extend([each+'d',each+'ed',each+each[-1]+'ed',each+'ing',each+each[-1]+'ing',each[:-1]+'ing'])
sup_methods = sup_methods + variations

ingredientObjects = []
for ing in ingredients:
    newIng = ingredient.Ingredient()
    lastWasNumber = False
    for word in ing.split():
        w = word.strip('(),')
        if w in fractions or w in numbers:
            newIng.addQuantity(w)
            lastWasNumber = True
        elif w in measurements and lastWasNumber:
            m = getattr(newIng, 'measurement')
            if m is None:
                setattr(newIng, 'measurement', w)
            lastWasNumber = False
        elif w in descriptors:
            newIng.addDescriptor(w)
            lastWasNumber = False
        elif w in sup_methods:
            newIng.addPreparation(w)
            lastWasNumber = False
        else:
            newIng.addName(w)
            lastWasNumber = False
    ingredientObjects.append(newIng)

# for i in ingredientObjects:
#     i.displayIngredient()

###################
# parse directions
###################

# list of methods
main_methods = ['saute','sautee','broil','boil','poach','grill','pan-fry','pan fry','stir-fry','stir fry','cook','deep-fry','deep fry','roast','bake','sear','simmer','steam','blanch','braise','stew','chill','freeze','refrigerate','toast','heat','fry','caramelize','charbroil','glaze','deglaze','microwave','nuke','frozen']

sup_methods = ['chop','grate','stir', 'shake', 'mince', 'crush', 'squeeze','mash','sprinkle'
        ,'season','dissolve','peel','seed','mix','grind','ground','dry','cure','grease','degrease'
        ,'dredge','dehydrate','dried','brush','fold','cut','stuff','ferment','flambe','foam','can'
        ,'paste','steep','infuse','dissolve','juice','marinate','soak','pasteurize','pickle'
        ,'puree','pure','reduce','reduction','separate','shir','smother','sous-vide','thicken','devein'
        ,'smash','tenderise','pit','slice','zest','spread','line','bread','toss','coat']

variations = []
for each in sup_methods:
    variations.extend([each+'d',each+'ed',each+each[-1]+'ed',each+'ing',each+each[-1]+'ing',each[:-1]+'ing'])
sup_methods = sup_methods + variations

variations_main = []
for each in main_methods:
    variations_main.extend([each+'d',each+'ed',each+each[-1]+'ed',each+'ing',each+each[-1]+'ing',each[:-1]+'ing'])
main_methods = main_methods + variations_main

cookingTools = ['pan','grater','rack','whisk','paper towel','tong','spatula','knife','oven','microwave','skillet','saucepan','pot','bowl','plate'
                ,'baking sheet','stovetop','knife','colander','strainer','aluminum foil','rolling pin','ladle','peeler','pastry bag'
                ,'blender','food processor','juicer','wok','dutch oven','convection oven','parchment paper','kettle','sheet pan'
                ,'brush','skewer','ricer','refrigerator','freezer','grill','press','torch','tray','pitter','slicer'
                ,'thermometer','scale','chopper','tenderiser','zester','slow cooker','baking dish','dish']
tools = []
for each in cookingTools:
    tools.extend([each+'s',each+'es'])
cookingTools = cookingTools + tools

ingredients_full = [x.split() for x in ingredients]

steps = {}

for i in range(len(directions)):
    steps[i+1] = {}
    for j in ingredients_full:
        for word in j[2:]:
            if word in directions[i].lower():
                if 'ingredients' in steps[i+1]:
                    if word not in steps[i+1]['ingredients']:
                        steps[i+1]['ingredients'].append(word)
                else:
                    steps[i+1]['ingredients'] = [word]
    for method in main_methods:
        if method in directions[i].lower():
            print directions[i]
            if 'methods' in steps[i+1]:
                if method not in steps[i+1]['methods']:
                    steps[i+1]['methods'].append(method)
            else:
                steps[i+1]['methods'] = [method]
    for method in sup_methods:
        if method in directions[i].lower():
            if 'prep_methods' in steps[i+1]:
                if method not in steps[i+1]['prep_methods']:
                    steps[i+1]['prep_methods'].append(method)
            else:
                steps[i+1]['prep_methods'] = [method]
    for tool in cookingTools:
        if tool in directions[i].lower():
            if 'tools' in steps[i+1]:
                if tool not in steps[i+1]['tools']:
                    steps[i+1]['tools'].append(tool)
            else:
                steps[i+1]['tools'] = [tool]

# for key, value in steps.items():
#     print "Step ", key,
#     for k in value:
#         print " ",k,
#         for v in value[k]:
#             print v

if transformation == 'vegetarian':
    meats = protein.meat_to_veg.keys()
    meats_used = []
    for ing in ingredientObjects:
        for meat in meats:
            if meat in getattr(ing, "name") or meat+'s' in getattr(ing,"name") or meat+'es' in getattr(ing,"name"):
                meats_used.append(meat)
                meats_used.append(meat+'s')
                meats_used.append(meat+'es')

    for ing in range(len(ingredientObjects)):
        i = getattr(ingredientObjects[ing], "name")
        newName = None
        for word in range(len(i)):
            for m in meats_used:
                if i[word].strip(',.()') == m:
                    if m[-1] == 's' and m[-2] == 'e':
                        newName = protein.meat_to_veg[m[:-2]]
                    elif m[-1] == 's':
                        newName = protein.meat_to_veg[m[:-1]]
                    else:
                        newName = protein.meat_to_veg[m]
        if newName is not None:
            if newName in protein.veg_quantities.keys():
                setattr(ingredientObjects[ing], "quantity", [protein.veg_quantities[newName]])
                setattr(ingredientObjects[ing], "measurement", "oz")
            ingredientObjects[ing].rename(newName)
            ingredientObjects[ing].clearPreparation()
            ingredientObjects[ing].clearDescriptor()

    newDirections = []

    for direction in directions:
        d = direction.split()
        for word in range(len(d)):
            for m in meats_used:
                if d[word].strip(',.()') == m or d[word].strip(',.()') == 'meat':
                    if m[-1] == 's' and m[-2] == 'e':
                        d[word] = protein.meat_to_veg[m[:-2]]
                    elif m[-1] == 's':
                        d[word] = protein.meat_to_veg[m[:-1]]
                    else:
                        d[word] = protein.meat_to_veg[m]
        d = [x for x in d if x not in protein.meat_parts]
        newDirections.append(d)

    for ing in ingredientObjects:
        ing.displayIngredient()

    for direction in newDirections:
        for word in direction:
            print word,
        print

elif transformation == 'meatify':
    meats = protein.meat_to_veg.keys()

    vegetarian_meats = {}
    for meat in meats:
        vegetarian_meats[protein.meat_to_veg[meat]] = meat

    vegetarian_meats_used = []
    for ing in ingredientObjects:
        for meat in vegetarian_meats:
            if meat in getattr(ing, "name") or meat+'s' in getattr(ing,"name") or meat+'es' in getattr(ing,"name"):
                vegetarian_meats_used.append(meat)
                vegetarian_meats_used.append(meat+'s')
                vegetarian_meats_used.append(meat+'es')

    for ing in range(len(ingredientObjects)):
        i = getattr(ingredientObjects[ing], "name")
        newName = None
        for word in range(len(i)):
            for m in vegetarian_meats_used:
                if i[word].strip(',.()') == m:
                    if m[-1] == 's' and m[-2] == 'e':
                        newName = vegetarian_meats[m[:-2]]
                    elif m[-1] == 's':
                        newName = vegetarian_meats[m[:-1]]
                    else:
                        newName = vegetarian_meats[m]
        if newName is not None:
            if newName in protein.veg_quantities.keys(): # <<<--- this needs to be fixed
                setattr(ingredientObjects[ing], "quantity", [protein.veg_quantities[newName]])
                setattr(ingredientObjects[ing], "measurement", "oz")
            ingredientObjects[ing].rename(newName)
            ingredientObjects[ing].clearPreparation()
            ingredientObjects[ing].clearDescriptor()

    newDirections = []

    for direction in directions:
        d = direction.split()
        for word in range(len(d)):
            for m in vegetarian_meats_used:
                if d[word].strip(',.()') == m or d[word].strip(',.()') == 'meat':
                    if m[-1] == 's' and m[-2] == 'e':
                        d[word] = vegetarian_meats[m[:-2]]
                    elif m[-1] == 's':
                        d[word] = vegetarian_meats[m[:-1]]
                    else:
                        d[word] = vegetarian_meats[m]
        d = [x for x in d if x not in protein.meat_parts] # <<<--- probably isnt necessary
        newDirections.append(d)

    for ing in ingredientObjects:
        ing.displayIngredient()

    for direction in newDirections:
        for word in direction:
            print word,
        print

elif transformation == 'healthy':
    health_foods = foodList.healthyIngredientsMap.keys()
    health_foods_used = []
    for ing in ingredientObjects:
        for health_food in health_foods:
            if health_food in ' '.join(getattr(ing, "name")):
                health_foods_used.append(health_food)
                break

    print "health foods used", health_foods_used

    for ing in range(len(ingredientObjects)):
        i = getattr(ingredientObjects[ing], "name")
        i = [x.strip(',.()') for x in i]
        i = ' '.join(i)
        newName = None
        for m in health_foods_used:
            if m in i:
                mList = m.split()
                i = i.split()
                locations = find_sub_list(mList, i)
                newName = foodList.healthyIngredientsMap[m]
                for loc in locations:
                    for j in range(loc[1] - loc[0] + 1):
                        if j == 0:
                            i[loc[0] + j] = newName
                        else:
                            i[loc[0] + 1] = ""
                i = ' '.join(i)
        if newName is not None:
            # ingredientObjects[ing].rename(newName)
            ingredientObjects[ing].rename(i)
            ingredientObjects[ing].clearPreparation()
            ingredientObjects[ing].clearDescriptor()

    newDirections = []

    for direction in directions:
        d = direction.split()
        d = [x.strip(',.()') for x in d]
        d = ' '.join(d)
        for m in health_foods_used:
            if m in d:
                mList = m.split()
                d = d.split()
                locations = find_sub_list(mList, d)
                newWord = foodList.healthyIngredientsMap[m]
                for loc in locations:
                    for i in range(loc[1] - loc[0] + 1):
                        if i == 0:
                            d[loc[0] + i] = newWord
                        else:
                            d[loc[0] + 1] = ""
                d = ' '.join(d)
        newDirections.append(d)

    for ing in ingredientObjects:
        ing.displayIngredient()

    for direction in newDirections:
        print direction

elif transformation == 'unhealthy':
    health_foods = foodList.healthyIngredientsMap.keys()  # <<<--- naming conventions backwards?

    unhealthy_foods = {}
    for health_food in health_foods:
        unhealthy_foods[foodList.healthyIngredientsMap[health_food]] = health_food

    unhealthy_foods_used = []
    for ing in ingredientObjects:
        for unhealthy_food in unhealthy_foods:
            if unhealthy_food in ' '.join(getattr(ing, "name")):
                unhealthy_foods_used.append(unhealthy_food)
                break

    print "health foods used", unhealthy_foods_used

    for ing in range(len(ingredientObjects)):
        i = getattr(ingredientObjects[ing], "name")
        i = [x.strip(',.()') for x in i]
        i = ' '.join(i)
        newName = None
        for m in unhealthy_foods_used:
            if m in i:
                mList = m.split()
                i = i.split()
                locations = find_sub_list(mList, i)
                newName = unhealthy_foods[m]
                for loc in locations:
                    for j in range(loc[1] - loc[0] + 1):
                        if j == 0:
                            i[loc[0] + j] = newName
                        else:
                            i[loc[0] + 1] = ""
                i = ' '.join(i)
        if newName is not None:
            # ingredientObjects[ing].rename(newName)
            ingredientObjects[ing].rename(i)
            ingredientObjects[ing].clearPreparation()
            ingredientObjects[ing].clearDescriptor()

    newDirections = []

    for direction in directions:
        d = direction.split()
        d = [x.strip(',.()') for x in d]
        d = ' '.join(d)
        for m in unhealthy_foods_used:
            if m in d:
                mList = m.split()
                d = d.split()
                locations = find_sub_list(mList, d)
                newWord = unhealthy_foods[m]
                for loc in locations:
                    for i in range(loc[1] - loc[0] + 1):
                        if i == 0:
                            d[loc[0] + i] = newWord
                        else:
                            d[loc[0] + 1] = ""
                d = ' '.join(d)
        newDirections.append(d)

    for ing in ingredientObjects:
        ing.displayIngredient()

    for direction in newDirections:
        print direction
else:
    cuisine_dict = {}
    if transformation == 'asian_to_italian':
        cuisine_dict = foodList.asianToItalian
    elif transformation == 'italian_to_asian':
        for asian_food in foodList.asianToItalian.keys():
            cuisine_dict[foodList.asianToItalian[asian_food]] = asian_food
    elif transformation == 'american_to_middle_eastern':
        cuisine_dict = foodList.americanToMiddleEastern
    elif transformation == 'middle_eastern_to_american':
        for american_food in foodList.americanToMiddleEastern.keys():
            cuisine_dict[foodList.americanToMiddleEastern[american_food]] = american_food
    elif transformation == 'mexican_to_soul_food':
        cuisine_dict = foodList.mexicanToSoulFood
    elif transformation == 'soul_food_to_mexican':
        for mexican_food in foodList.mexicanToSoulFood.keys():
            cuisine_dict[foodList.mexicanToSoulFood[mexican_food]] = mexican_food
    elif transformation == 'french_to_indian':
        cuisine_dict = foodList.frenchToIndian
    elif transformation == 'indian_to_french':
        for indian_food in foodList.frenchToIndian.keys():
            cuisine_dict[foodList.frenchToIndian[indian_food]] = indian_food

    cuisine_foods = cuisine_dict.keys()
    cuisine_foods_used = []
    for ing in ingredientObjects:
        for cuisine_food in cuisine_foods:
            if cuisine_food in ' '.join(getattr(ing, "name")):
                cuisine_foods_used.append(cuisine_food)
                break

    print "cuisine foods used", cuisine_foods_used

    for ing in range(len(ingredientObjects)):
        i = getattr(ingredientObjects[ing], "name")
        i = [x.strip(',.()') for x in i]
        i = ' '.join(i)
        newName = None
        for m in cuisine_foods_used:
            if m in i:
                mList = m.split()
                i = i.split()
                locations = find_sub_list(mList, i)
                newName = cuisine_dict[m]
                for loc in locations:
                    for j in range(loc[1] - loc[0] + 1):
                        if j == 0:
                            i[loc[0] + j] = newName
                        else:
                            i[loc[0] + 1] = ""
                i = ' '.join(i)
        if newName is not None:
            # ingredientObjects[ing].rename(newName)
            ingredientObjects[ing].rename(i)
            ingredientObjects[ing].clearPreparation()
            ingredientObjects[ing].clearDescriptor()

    newDirections = []

    for direction in directions:
        d = direction.split()
        d = [x.strip(',.()') for x in d]
        d = ' '.join(d)
        for m in cuisine_foods_used:
            if m in d:
                mList = m.split()
                d = d.split()
                locations = find_sub_list(mList, d)
                newWord = cuisine_dict[m]
                for loc in locations:
                    for i in range(loc[1] - loc[0] + 1):
                        if i == 0:
                            d[loc[0] + i] = newWord
                        else:
                            d[loc[0] + 1] = ""
                d = ' '.join(d)
        newDirections.append(d)

    for ing in ingredientObjects:
        ing.displayIngredient()

    for direction in newDirections:
        print direction
