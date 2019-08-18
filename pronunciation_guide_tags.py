from log_into_wiki import *
import mwparserfromhell

site = login('bot', 'lol')  # Set wiki
summary = 'Bot Edit'  # Set summary

this_name = 'Daedalus'
this_user = 'Benvarmeren'

limit = -1
startat_page = None
print(startat_page)
# startat_page = 'File:ElogudenDanish.mp4'
this_template = site.pages['Template:PlayerPronunciationFile']  # Set template
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
	if not passed_startat:
		print("Skipping page %s" % page.name)
		continue
	lmt += 1
	text = page.text()
	wikitext = mwparserfromhell.parse(text)
	for template in wikitext.filter_templates():
		if tl_matches(template, ['PlayerPronunciationFile']):
			if template.get('recordedby').value.strip() == this_name:
				template.add('user', this_user)
				template.add('language', 'Danish')
				template.add('native', 'Yes')
	
	newtext = str(wikitext)
	if text != newtext:
		print('Saving page %s...' % page.name)
		page.save(newtext, summary=summary)
	else:
		print('Skipping page %s...' % page.name)
