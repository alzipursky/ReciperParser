import requests, bs4
import string

recipeUrl = 'http://allrecipes.com/recipe/220128/chef-johns-buttermilk-fried-chicken/'

# get webpage
res = requests.get(recipeUrl)
res.raise_for_status()
recipe = bs4.BeautifulSoup(res.text,"html.parser")

# get ingredients --->>> there's extra stuff on the end we don't want
ingredients = []
for word in recipe.findAll("span", { "class" : "recipe-ingred_txt" }):
    ingredients.append(word.get_text())
    # print word.get_text()
ingredients_full = [x.split() for x in ingredients]

# get directions
directions = []
for word in recipe.findAll("span", { "class" : "recipe-directions__list--item" }):
    directions.append(word.get_text())
    # print word.get_text()

# list of methods
main_methods = ['saute','sautee','broil','boil','poach','grill','pan-fry','pan fry','stir-fry','stir fry','deep-fry','deep fry','roast','bake','sear','simmer','steam','blanch','braise','stew','chill','freeze','refrigerate','toast','heat','fry','caramelize','charbroil','glaze','deglaze','microwave','nuke','frozen']

sup_methods = ['chop','grate','stir', 'shake', 'mince', 'crush', 'squeeze','sprinkle','season','dissolve','peel','seed','mix','grind','ground','dry','cure','grease','degrease','dredge','dehydrate','dried','brush','fold','cut','stuff','ferment','flambe','foam','can','paste','steep','infuse','dissolve','juice','marinate','soak','pasteurize','pickle','puree','pure','reduce','reduction','separate','shir','smother','sous-vide','thicken','devein']

variations = []
for each in sup_methods:
    variations.extend([each+'d',each+'ed',each+each[-1]+'ed',each+'ing',each+each[-1]+'ing',each[:-1]+'ing'])
sup_methods = sup_methods + variations
print len(sup_methods)


steps = {}

for i in range(len(directions)):
    steps[i+1] = {}
    for j in ingredients_full:
        for word in j[2:]:
            if word in directions[i]:
                if 'ingredients' in steps[i+1]:
                    if word not in steps[i+1]['ingredients']:
                        steps[i+1]['ingredients'].append(word)
                else:
                    steps[i+1]['ingredients'] = [word]

for key, value in steps.items():
    print "Step ", key,
    for k in value:
        print " ",k,
        for v in value[k]:
            print v

