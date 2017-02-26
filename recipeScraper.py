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
title = []
for word in recipe.findAll("h1", {"class" : "recipe-summary__h1"}):
    title.append(word.get_text())
    # print word.get_text()
print title

# get ingredients --->>> there's extra stuff on the end we don't want
ingredients = []
for word in recipe.findAll("span", { "class" : "recipe-ingred_txt" }):
    ingredients.append(word.get_text())
    # print word.get_text()
print ingredients

# get prep time
prepTime = []
for word in recipe.findAll("time", { "itemprop" : "prepTime" }):
    prepTime.append(word.get_text())
    # print word.get_text()
print prepTime

# get cook time
cookTime = []
for word in recipe.findAll("time", { "itemprop" : "cookTime" }):
    cookTime.append(word.get_text())
    # print word.get_text()
print cookTime

# get total time
totalTime = []
for word in recipe.findAll("time", { "itemprop" : "totalTime" }):
    totalTime.append(word.get_text())
    # print word.get_text()
print totalTime

# get directions
directions = []
for word in recipe.findAll("span", { "class" : "recipe-directions__list--item" }):
    directions.append(word.get_text())
    # print word.get_text()
print directions

# get footnotes
footnotes = []
for word in recipe.findAll("section", {"class" : "recipe-footnotes"})[0].findAll("li"):
    footnotes.append(word.get_text())
    # print word.get_text()
print footnotes
