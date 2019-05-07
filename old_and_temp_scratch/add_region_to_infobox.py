import mwparserfromhell
from log_into_wiki import *
limit = -1

region = 'Korea'

site = login('bot','lol')

with open('pages.txt') as f:
	lines = f.readlines()
pages = [site.pages[p.strip()] for p in lines]

lmt = 0
for p in pages:
	if lmt == limit:
		break
	lmt += 1
	text = p.text()
	wikitext = mwparserfromhell.parse(text)
	templates = wikitext.filter_templates()
	for template in templates:
		if template.name.matches('Infobox Tournament'):
			template.add('region',region)
	newtext = str(wikitext)
	if text != newtext:
		print('Saving page %s...' % p.name)
		p.save(newtext,summary = 'Auto-adding region (%s)' % region)