import requests, bs4, sys, ingredient, protein, foodList


def find_sub_list(sl,l):
    results=[]
    sll=len(sl)
    for ind in (i for i,e in enumerate(l) if e==sl[0]):
        if l[ind:ind+sll]==sl:
            results.append((ind,ind+sll-1))

    return results

if len(sys.argv) != 3:
    print "usage: python recipeScraper.py <url of recipe in single quotes>"
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

if transformation == 'healthy':
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
