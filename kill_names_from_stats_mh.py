from log_into_wiki import *
import mwparserfromhell

site = login('bot', 'lol')  # Set wiki
summary = 'Remove redundant parameters from templates'  # Set summary

limit = -1
startat_page = None
print(startat_page)
#startat_page = 'SirNukesAlot/Statistics'

this_templates = [
	#'CareerPlayerStats',
	#'PlayerYearStats',
	'YearTeamStats'
]

for this_template in this_templates:
	this_template_page = site.pages['Template:' + this_template]  # Set template
	pages = this_template_page.embeddedin()
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
			if template.name.matches(this_template):
				if template.has(1):
					if page.name.startswith(template.get(1).value.strip() + '/'):
						template.remove(1)
		newtext = str(wikitext)
		if text != newtext:
			print('Saving page %s...' % page.name)
			page.save(newtext, summary=summary)
		else:
			print('Skipping page %s...' % page.name)