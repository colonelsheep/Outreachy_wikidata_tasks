import pywikibot
from pywikibot.data import api
from pywikibot import pagegenerators
import urllib.request
import re

#connects to wikidata
wd_connect = pywikibot.Site('wikidata', 'wikidata')
wd = wd_connect.data_repository()
search_count = input("How many articles to search through? ")
author_family_name = None
author_given_name = None

#creates a SPARQL query to get a number of articles that include a ResearchGate citation and any authors or author name strings
def get_researchgate_wikidata():
    sparql = """SELECT DISTINCT ?item ?itemLabel WHERE {
    SERVICE wikibase:label { bd:serviceParam wikibase:language \"[AUTO_LANGUAGE]\". }
    {
        SELECT DISTINCT ?item WHERE {
        ?item p:P5875 ?statement0.
        ?statement0 (ps:P5875) _:anyValueP5875.
        {
            ?item p:P2093 ?statement1.
            ?statement1 (ps:P2093) _:anyValueP2093.
         }
        UNION
        {
            ?item p:P50 ?statement2.
            ?statement2 (ps:P50/(wdt:P279*)) _:anyValueP50.
        }
        }
        LIMIT""" + search_count + " }}"  
    generator = pagegenerators.WikidataSPARQLPageGenerator(sparql, site=wd)
    for page in generator:
        get_researchgate_url(page)

#gets the researchgate url for for a wikidata page
def get_researchgate_url(page):
    wd_info = page.get()
    print("\n------------------------------------------------------------------------------------------------------------\n")
    print("Adding author given names and author last names to: " + page.title() + " (" + wd_info['labels']['en'] + ")")
    
    #gets researchgate API url to download bibtex
    for rid in wd_info['claims']['P5875']:
        researchgate_id = rid.getTarget().title()
    rid_url = 'https://www.researchgate.net/lite.publication.PublicationDownloadCitationModal.downloadCitation.html?fileType=BibTeX&citation=citation&publicationUid=' + researchgate_id
    bibtex = get_bibtex(rid_url)
    get_author_names(bibtex)
    get_author_info(wd_info, 'P50')
    get_author_info(wd_info, 'P2093')


#gets bibtex from bibtex download API url
def get_bibtex(rid_url):
    user_agent = 'User_Agent'
    headers = {'User-Agent':user_agent}
    req = urllib.request.Request(rid_url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            #utf-8 conversion necessary to properly read accented and other special chars
            html = response.read().decode('utf-8')

    return str(html)

#get author given and family names through regex
def get_author_names(bibtex):
    authors = re.search(r'author = {(.*?)}', bibtex)
    global author_family_name
    global author_given_name
    #family names are preceded by 'and ' or '{' for first name case and ending with ','
    author_family_name = re.findall(r'(?:and |{)(.*?)(?=,)', authors.group())
    #given names are preceded by a ', ' and end with ' and' or '}'
    author_given_name = re.findall(r'(?:, )(.*?)(?= and|})', authors.group())

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
    else:
        print(pid + " already in author info!")

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
            #gets bibTeX given and family name from series ordinal position, equivalent to author placement in bibTeX list
            try:
                given_name = author_given_name[int(series_ordinal) - 1]
                family_name = author_family_name[int(series_ordinal) - 1]
            except:
                print("This array size isn't correct! Check over any edits to make sure they're accurate.")
            print("BibTeX author name: " + given_name + " " + family_name)
            #adds stated as name if author and not in author page
            if pid == 'P50':
                add_qualifier(claim, given_name + " " + family_name, 'P1932')
            #adds author given name and author family name if not in author page
            add_bibtex_qualifiers(claim, given_name, family_name)

#adds 'stated as', 'author given names', and 'author family names' to author
def add_bibtex_qualifiers(claim, given_name, family_name):
            add_qualifier(claim, given_name, 'P9687')
            add_qualifier(claim, family_name, 'P9688')

get_researchgate_wikidata()
