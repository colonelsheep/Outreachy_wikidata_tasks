import pywikibot
from pywikibot.data import api
from pywikibot import pagegenerators
import requests

#connect to wikidata
wd_connect = pywikibot.Site('wikidata', 'wikidata')
wd = wd_connect.data_repository()

#input an integer. Will be number of articles searched
page_count = input("How many articles to search through? ")

#stores all parts of a name that are
#not clearly given names or family names (for all names searched)
suspicious_names = []

#stores all parts of a name that were not added
unfound_names = []

#stores all edits made
added_names = []

#edits a wikidata page
#from https://github.com/mpeel/wikicode/blob/master/example.py 74-88
def edit_wiki_data(wd_item, propertyid, value):
    item_dict = wd_item.get()
    claim_target = pywikibot.ItemPage(wd, value)
    new_claim = pywikibot.Claim(wd, propertyid)
    new_claim.setTarget(claim_target)

    print(new_claim)
    will_add_claim = input("Add to page? ")
    if will_add_claim == 'y':
        wd_item.addClaim(new_claim, summary='Added name to page')
        added_names.append(item_dict['labels']['en'] + " (" + wd_item.title() + "): " + claim_target.get()['labels']['en'])
        print("View edit at page: " + wd_item.title())

#searches wikidata - unsure how to set the number of articles it returns!
#from  https://gist.github.com/ettorerizza/7eaebbd731781b6007d9bdd9ddd22713 
def search_wiki_data(site, itemtitle):
    params =  { 'action' : 'wbsearchentities',
            'format' : 'json',
            'language' : 'en',
            'type' : 'item',
            'search' : itemtitle }
    request = api.Request(site = site, parameters = params)
    return request.submit()

#gets list of articles to get authors from
def get_page_for_author_search():
	#selects scholarly articles that contain authors
	sparql = "SELECT DISTINCT ?item WHERE {?item p:P50 ?statement0. ?statement0 (ps:P50/(wdt:P279*)) _:anyValueP50. ?item p:P31 ?statement1. ?statement1 (ps:P31/(wdt:P279*)) wd:Q13442814. } LIMIT " + page_count
	generator = pagegenerators.WikidataSPARQLPageGenerator(sparql, site=wd)
	for page in generator:
		get_page_authors(page)


#gets all authors for a given page
def get_page_authors(wd_page):
    wd_page_info = wd_page.get()
    print ("\nSearching for authors in: " + wd_page_info['labels']['en'])
    try:
        for author in wd_page_info['claims']['P50']:
            p50_value = author.getTarget()
            p50_dict = p50_value.get()
            print("\nGoing to author page " + p50_value.title() + ": " + p50_dict['labels']['en'])
            author_page = pywikibot.ItemPage(wd, p50_value.title())
            get_page_names(author_page)
    except:
        print("No authors in this page!")

#gets name information for a given page
def get_page_names(wd_page):
    wd_page_info = wd_page.get()
    #splits title (equivalent to full author name) into an array.
    #first element will always be a given name, last one will (almost!) always be a family name.
    #other elements (if exist) are less clear and not dealt with by this program (for now!)
    name_split = wd_page_info['labels']['en'].split()
    qid = wd_page.title()

    #if non-obvious name properties in array exist, add to suspicious_names
    if len(name_split) > 2:
        for name_part in name_split[1:-1]:
            suspicious_names.append(wd_page_info['labels']['en'] + " (" + qid + "): " + name_part)

    #if given name property exists in page, print it
    try:
        for given_name in wd_page_info['claims']['P735']:
             p735_value = given_name.getTarget()
             p735_dict = p735_value.get()
             print( "This person already has a given name " + p735_value.title() + ": " + p735_dict['labels']['en'])

    #if it does not exist, try to add it
    except:
        print("No given name in this page! Let's add it.")
        add_given_name = get_name_from_search(name_split[0], 'given name')
        if not add_given_name == 'None':
            edit_wiki_data(wd_page, 'P735', add_given_name)
	#if given name not found in search, add to unfound_name list to potentially manually add later
        else:
            unfound_names.append("Unadded given name in " + wd_page_info['labels']['en'] + " (" + qid + "): " + name_split[0])
    #if family name property exists in page, print it 
    try:
        for family_name in wd_page_info['claims']['P734']:
            p734_value = family_name.getTarget()
            p734_dict = p734_value.get()
            print("This person already has a family name " + p734_value.title() + ": " + p734_dict['labels']['en'])

    #if it does not exist, try to add it
    except:
        print("No family name in this page! Let's add it.")
        add_family_name = get_name_from_search(name_split[-1], 'family name')
        if not add_family_name == 'None':
            edit_wiki_data(wd_page, 'P734', add_family_name)
	#if family name not found in search, add to unadded_name list to potentially manually add later
        else:
            unfound_names.append("Unadded family name in " + wd_page_info['labels']['en'] + " (" + qid + "): " + name_split[-1])

#searches for a provided family name/given name
def get_name_from_search(name, name_type):
    search = search_wiki_data(wd, name)
    try:
        if search['search'] != []:
            for search_results in search['search']:
                #if search result has a family name/given name, check if its correct
                if name_type in search_results['description']:
                    print(search_results['display']['label']['value'] + ": " + search_results['description'])
                    is_name = input("Is this the correct name? ")
                    if (is_name == 'y'):
			#returns name ID if found
                        return search_results['id']
                  
                    return 'None'

            print("Name not found!")
            return 'None'
        else:
            print("Name not found!")
            return 'None'
    except:
        print("Name not found!")
        return 'None'


get_page_for_author_search()   

#prints all non-obviously given name/family name name parts
print("\nSUSPICIOUS NAMES:")
print('\n'.join(suspicious_names))

#prints all names that weren't found in search
print("\nUNADDED NAMES:")
print('\n'.join(unfound_names))

#prints all edits made
print("\nADDED NAMES:")
print('\n'.join(added_names))
