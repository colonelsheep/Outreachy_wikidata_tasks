import pywikibot
from pywikibot.data import api

wd_connect = pywikibot.Site("wikidata", "wikidata")
wd = wd_connect.data_repository()
outreachy_page = pywikibot.Page(wd_connect, 'User:PangolinMexico/Outreachy_1')
sand_box = pywikibot.ItemPage(wd, 'Q4115189')
articles = ['Q45962899', 'Q39570994', 'Q38667946', 'Q40407003', 'Q73194982', 'Q37640097', 'Q33632880', 'Q95643353', 'Q76507957', 'Q67382053', 'Q67062045', 'Q43192398']

#Based on https://github.com/mpeel/wikicode/blob/master/example.py lines 23 to 32


#Prints a wikidata page 
def print_page(page):
    text = page.get()
    print(text)


#gets a given qualifier's value
def get_qualifier_value(claim, pid):
    value = claim.qualifiers.get(pid)[0].target
    return(value)

#prints all properties for a given page
def print_properties(wd_page):
    wd_page_info = wd_page.get()
    print(wd_page_info['labels']['en'])
    try:
        for claim in wd_page_info['claims']:
            #gets property information
            property_page = pywikibot.PropertyPage(wd_connect, claim)
            property_dict = property_page.get()
            property_title = property_dict['labels']['en']
            #gets claim value
            claim_value = wd_page_info['claims'][claim][0].getTarget()
            #if claim leads to wikidata page, act accordingly
            try:
                claim_dict = claim_value.get()
                claim_qid = claim_value.title()
                claim_title = claim_dict['labels']['en']
            #else, convert to string (this could be improved upon but the sandbox pages changes too much! 
            # adding specific value info might break the whole program. so i'm leaving this as is.)
            except:
                claim_qid = ""
                claim_title = str(claim_value)
            #print property title followed by claim, id if exists, and title as obtained
            print(property_title + " (" + claim + ") " + claim_qid + ": " + claim_title) 
    except:
        print("No claims in this page!")

#prints all author string names and gets all authors for a given page
def get_page_authors(wd_page):
    wd_page_info = wd_page.get()
    print("\n" + wd_page_info['labels']['en'])
    if 'P50' in wd_page_info['claims']:
        for author in wd_page_info['claims']['P50']:
            p50_value = author.getTarget()
            p50_dict = p50_value.get()
            series_ordinal = get_qualifier_value(author, 'P1545')
            print(series_ordinal + ") Author " + p50_value.title() + ": " + p50_dict['labels']['en'] )
            author_page = pywikibot.ItemPage(wd, p50_value.title())
            get_page_names(author_page)
    if 'P2093' in wd_page_info['claims']:
        for author_name_string in wd_page_info['claims']['P2093']:
            p2093_value = author_name_string.getTarget()
            series_ordinal = get_qualifier_value(author_name_string, 'P1545')
            print(series_ordinal + ") Author Name String: " + p2093_value)

#gets name information for a given page
def get_page_names(wd_page):
    wd_page_info = wd_page.get()
    qid = wd_page.title()
    #if given name property exists in page, print it
    try:
        for given_name in wd_page_info['claims']['P735']:
             p735_value = given_name.getTarget()
             p735_dict = p735_value.get()
             print( "Given name " + p735_value.title() + ": " + p735_dict['labels']['en'])
    except:
        print("No given name in this page!")
    #if family name property exists in page, print it 
    try:
        for family_name in wd_page_info['claims']['P734']:
            p734_value = family_name.getTarget()
            p734_dict = p734_value.get()
            print("Family name " + p734_value.title() + ": " + p734_dict['labels']['en'])
    except:
        print("No family name in this page!")
        

#1) Print Outreachy page, then edit to add hello
print("\nTASK ONE:")
def add_hello(page):
    print_page(page)
    text = page.get()
    text = text + "\nHello!"
    page.text = text
    try:
        page.save("Edit saved!")
        return 1
    except:
        print("Error! Page not saved!")
        return 0

add_hello(outreachy_page)

#2) Print Sandbox info
print("\nTASK TWO:")
print_properties(sand_box)

#3) Print out all author information for articles in Outreachy 1, as well as the name info on author pages
print("\nTASK THREE:")
for article in articles:
    article_page = pywikibot.ItemPage(wd, article)
    get_page_authors(article_page)
