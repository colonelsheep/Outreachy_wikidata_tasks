import pywikibot
from pywikibot.data import api

site = pywikibot.Site("wikidata", "wikidata")
repo = site.data_repository()
taskOne = pywikibot.Page(site, 'User:PangolinMexico/Outreachy_1')

repo = site.data_repository()
sandBox = pywikibot.ItemPage(repo, 'Q4115189')
articlePage = pywikibot.ItemPage(repo, 'Q57602599')

#Based on https://github.com/mpeel/wikicode/blob/master/example.py lines 23 to 32
def addHello(page):
    text = page.get()
    text = text + "\nHello!"
    page.text = text
    try:
        page.save("Edit saved!")
        return 1
    except:
        print("Error! Page not saved!")
        return 0

#Prints a wikidata page 
def printPage(page):
    text = page.get()
    print(text)


#Prints information from sandbox
def printSandBoxInfo(page):
    info = page.get()
    print(info.keys())
    print(info["claims"])

#Print author info
def printAuthorInfo(page):
    info = page.get()
    authorArray = []
    for claim in info['claims']['P31']:
        authorValue = claim.getTarget()
        authorName = authorValue.get()
        print(authorValue.title())
        print(authorName['labels']['en'])
        
def chooseTask(choice):
    if(int(choice) == 1):
        printPage(taskOne)
    elif (int(choice) == 2):
        printSandBoxInfo(sandBox)
    elif(int(choice) == 3):
        printAuthorInfo(articlePage)
    else:
       userChoice = input("Invalid input! Let's try that again.")
       chooseTask(userChoice)

userChoice = input("Type 1 to print my Outreachy_1 page. Type 2 to print out information about the andbox.")

chooseTask(userChoice)
