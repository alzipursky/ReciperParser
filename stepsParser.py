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

directions = [each.split('.')[0] for each in directions]

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

for key, value in steps.items():
    print "Step ", key,
    for k in value:
        print " ",k,
        for v in value[k]:
            print v

