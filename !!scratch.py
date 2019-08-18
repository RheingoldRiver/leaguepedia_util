from log_into_wiki import *
import mwparserfromhell

site = login('bot', 'lol')  # Set wiki
summary = 'Remove notab from playoffs pages'  # Set summary

limit = -1
startat_page = None
print(startat_page)
# startat_page = 'asdf'
this_template = site.pages['Template:MatchRecap/Button']  # Set template
pages = this_template.embeddedin()

# with open('pages.txt', encoding="utf-8") as f:
# 	pages = f.readlines()

passed_startat = False if startat_page else True
lmt = 0
for page in pages:
	if lmt == limit:
		break
	if startat_page and page.name == startat_page:
		passed_startat = True
	if not '/Playoffs' in page.name:
		print("Skipping page %s" % page.name)
		continue
	if not passed_startat:
		print("Skipping page %s" % page.name)
		continue
	lmt += 1
	text = page.text()
	wikitext = mwparserfromhell.parse(text)
	for template in wikitext.filter_templates():
		if tl_matches(template, ['MatchRecap/Button']):
			if template.has('notab'):
				template.remove('notab')
	
	newtext = str(wikitext)
	if text != newtext:
		print('Saving page %s...' % page.name)
		page.save(newtext, summary=summary)
	else:
		print('Skipping page %s...' % page.name)
