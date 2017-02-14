import requests, bs4, sys

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
for word in recipe.findAll("h1", {"class" : "recipe-summary__h1"}):
    print word.get_text()

# get ingredients --->>> there's extra stuff on the end we don't want
for word in recipe.findAll("span", { "class" : "recipe-ingred_txt" }):
    print word.get_text()

# get prep time
for word in recipe.findAll("time", { "itemprop" : "prepTime" }):
    print word.get_text()

# get cook time
for word in recipe.findAll("time", { "itemprop" : "cookTime" }):
    print word.get_text()

# get total time
for word in recipe.findAll("time", { "itemprop" : "totalTime" }):
    print word.get_text()

# get directions
for word in recipe.findAll("span", { "class" : "recipe-directions__list--item" }):
    print word.get_text()

# get footnotes
for word in recipe.findAll("section", {"class" : "recipe-footnotes"})[0].findAll("li"):
    print word.get_text()
