import threading, mwparserfromhell
from log_into_wiki import *

site = login('me','lol')
blankedit = False
thispage = site.pages['Samsung Galaxy']
timeoutLimit = 30
pages = thispage.backlinks()

def processtemplate(tl):
	for param in tl.params:
		if param.value.strip().lower() == 'ss':
			tl.add(param.name,'Samsung Galaxy')

def savepage(targetpage, savetext):
	targetpage.save(savetext, summary='SS to Samsung Galaxy')

for page in pages:
	print("Processing next page: " + page.name)
	text = page.text()
	origtext = text
	# do links first because it's easier to just edit them as a string
	wikitext = mwparserfromhell.parse(text)
	for template in wikitext.filter_templates():
		processtemplate(template)
	newtext = str(wikitext)
	if origtext != newtext or blankedit:
		print("Saving...")
		t = threading.Thread(target=savepage, kwargs={"targetpage": page, "savetext": newtext})
		t.start()
		t.join(timeout=timeoutLimit)
	else:
		print("No changes, skipping")