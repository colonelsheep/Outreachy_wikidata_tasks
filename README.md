# Outreachy_wikidata
This is my work for Wikimedia's contribution section of Outreachy 24. 
I am working on Task T300207: What's in a name? Automatically identifying first and last author names for Wikicite and Wikidata.

If you're also working on this task, feel free to send me a message to ask for help/talk things through! 

You can find me on Zulip at garciamtz00@gmail.com, or on WikiData at PangolinMexico.

# task_two
This folder contains my work for Task 2.

## task_two.py
This script fulfills all requirements as set out by Task 2. 
1. It prints out my task 1 page and edits it
2. It prints out all property information in the WikiData sandbox page (this could be improved by more neatly working with values that are not WikiData items... I wasn't sure how to do this without potentially breaking my code if new edits are made to the sandbox!)
3. It prints out all author information from my 12 articles in Task 1, then automatically goes to their author pages (if they exists) and prints out their given names/family names (if they exist.)

See example output at task_two_output.txt

## auto_add_name.py
I got really into pywikibot, so decided to see if I could write a script that automatically adds missing given and family names to author pages with missing info. I managed to do it! Here's how it works:
1. Asks the user how many articles to search through (``page_count`` input variable)
2. Begins by querying articles with **P31** (instance of) = **Q13442814** (scholarly article) that have at least one **P50** (author) statement (``get_page_for_author_search``)
3. Goes to the author page of each author in each article (``get_page_authors``)
4. Splits the author page title into a list, where the first element will almost always be a given name and the last element will almost always be a family name. If more elements appear, add them to a list of 'suspicious names' to potentially manually add or correct edits later (These will be middle names, Latin American surnames, etc.) (``get_page_names``)
5. Checks if given names/family names already exist in the author page. If they do, print them and move onto the next author. 
6. If they don't, try to add them by searching the first element of the list, or the last element of the list if adding a given name/family name, respectively. (``get_name_from_search``)
7. If name found, edit wikidata to add name (``edit_wiki_data``). Else, do not add to wikidata and add to a list with all unfound names.
8. When done searching through all articles, print all "suspicious name" parts, all unfound names, and all edits made.

See example output at auto_add_name_output.txt

I am very proud of this script, and can see it working well in my contributions for wikidata! However, there are definitely ways it could be improved, as well as possible next steps:
### Things to improve
1. Currently, the query that obtains scholarly articles often gets articles that have already been obtained in previous runs of the script. This could potentially be improved by only getting articles that we *know* have authors that are missing given names/family names, or by getting a large sample size and randomising its order, then only going through a section of the randomised result. There could also be ways to get random results of a query (as opposed to ordered results) but I had difficulty finding any examples of this.
2. This script is very catered for Western names that only have 1 given name and 1 family name. I try to improve this by automatically adding every other part of a name to a list that is printed at the end, which allows for the user to manually evaluate and add these parts of a name themselves. I wonder if there are ways to detect whether the "middle parts" of a name are surnames, middle names, or something else: I was thinking of potentially going through a search of these parts as both given names and family names, and letting the user decide if the output seems correct... but I thought it lent itself to too much human error.
3. This script could be much more automated than it already is... I was just afraid of doing this! One way to automate it more would be to automatically check if the item returned by the name search matches the search exactly, and only accept it if it does... but this removes potential acceptable names that aren't *exactly* the same.
4. Sometimes family names/given names that do exist on wikidata aren't found because the search query only goes through a certain number of articles. I couldn't figure out a way to optimise this... but I'm sure it's possible!

### Possible next steps
1. The obvious next step is to create a script that not only adds already existing given names/family names to authors, but makes *new* name pages if they do not exist. This wouldn't be too hard, but due to error 4 mentioned above I was worried I would be adding names that already exist. I would also need to become *very confident* in the statements a name page needs before adding this. This would also be particularly difficult with names that need special statements, such as kanji.
2. Double-barrelled surnames are almost never found because they almost never exist! These would be much easier to make than entirely new names, and could be detected via a RegEx. From here, the two parts of the family name could be searched, and if found, compounded to make a page for the double barrelled surname.
3. Where a name comes from is one of the hardest parts to automate... maybe by adding large databases of common names this could be improved? Using ML to detect where names come from? I'm not sure.
4. Maybe generalise this to just search for authors instead of scientific articles? Might make the program more efficient.

# task_three
This folder contains my work for Task 3.

See example output at task_three_output.txt
