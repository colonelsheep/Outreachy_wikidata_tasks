import urllib.request
import pywikibot
import re

#get response from citation url
with urllib.request.urlopen('https://ui.adsabs.harvard.edu/abs/2004SPIE.5498...11R/exportcitation') as response:
    html = response.read()
#RegEx that gets author bibTeX authors by identifying 'author = {' as beginning and '}\n' as end of tag
authors = re.search(r'author = {(.*?)},\\n', str(html))
#creates list that gets all given names using authors RegEx
#identifies '},' as end of family name and text 'and' or '},\\n' for end of given name
author_given_name = re.findall(r'}, (.*?)(?: and|},\\n)', authors.group())
#creates list that gets all family names using authors RegEx
#identifies '{' as beginning of family name and '}' as end of family name. uses group 1 so first family name parsed correctly
author_family_name = re.findall(r'{(.*?)}', authors.group(1))
#connect to wikidata, get south pole telescope page
wd_connect = pywikibot.Site("wikidata", "wikidata")
wd = wd_connect.data_repository()
south_pole_telescope = pywikibot.ItemPage(wd, 'Q55893751')

#gets a given qualifier's value
def get_qualifier_value(claim, pid):
    value = claim.qualifiers.get(pid)[0].target
    return(value)

#adds qualifier with P = pid, Q = value, to claim
def add_qualifier(claim, value, pid):
    if pid not in claim.qualifiers:
        qualifier = pywikibot.Claim(wd, pid)
        qualifier.setTarget(value)
        claim.addQualifier(qualifier, summary='Adding qualifier' + pid)
        print("Added " + pid + ": " + value)

#gets + prints all author info for both authors and author name strings
def get_author_info(page, pid):
    if pid in page['claims']:
        for claim in page['claims'][pid]:
            claim_value = claim.getTarget()
            #gets series ordinal for author
            series_ordinal = get_qualifier_value(claim, 'P1545')
            #if author/wiki-item page
            try:
                claim_dict = claim_value.get()
                print(series_ordinal + ") Author " + claim_value.title() + ": " + claim_dict['labels']['en'])
            #if author name string/other string value
            except:
                print(series_ordinal + ") Author Name String: " + claim_value)
            #gets bibTeX given and family name from series ordinal position, equivalent to author placement in BibTex list
            given_name = author_given_name[int(series_ordinal) - 1]
            family_name = author_family_name[int(series_ordinal) - 1]
            print("BibTeX author name: " + given_name + " " + family_name)
            #adds qualifiers if not in author page
            add_bibtex_qualifiers(claim, given_name, family_name)

#adds 'stated as', 'author given names', and 'author family names' to author
def add_bibtex_qualifiers(claim, given_name, family_name):
            add_qualifier(claim, given_name + " " + family_name, 'P1932')
            add_qualifier(claim, given_name, 'P9687')
            add_qualifier(claim, family_name, 'P9688')

#gets wikidata page info, prints title, and proceeds to print author info and add bibtex qualifiers 
def task_three(wd_page):
    wd_page_info = wd_page.get()
    print(wd_page_info['labels']['en'])
    get_author_info(wd_page_info, 'P50')
    get_author_info(wd_page_info, 'P2093')


task_three(south_pole_telescope)
