import requests, bs4, sys, ingredient

if len(sys.argv) != 2:
    print "usage: python recipeScraper.py <url of recipe in single quotes>"
    quit()

args = sys.argv

recipeUrl = args[1]

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
# print directions

# get footnotes
footnotes = []
for word in recipe.findAll("section", {"class" : "recipe-footnotes"})[0].findAll("li"):
    footnotes.append(word.get_text())
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

for i in ingredientObjects:
    i.displayIngredient()
