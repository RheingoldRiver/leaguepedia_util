from log_into_wiki import *
import mwparserfromhell

site = login('me', 'lol')  # Set wiki
summary = 'Attempting to migrate content to data ns'  # Set summary

limit = -1
startat_page = None
print(startat_page)
# startat_page = 'asdf'
this_template = site.pages['Template:ExternalContent/Line']  # Set template
pages = this_template.embeddedin()

tabs_templates = ['TDRight', 'TabsDynamic', 'TD']

passed_startat = False if startat_page else True
lmt = 0
for page in pages:
	if lmt == limit:
		break
	if startat_page and page.name == startat_page:
		passed_startat = True
	if page.name.startsith('Data:'):
		continue
	if not passed_startat:
		print("Skipping page %s" % page.name)
		continue
	lmt += 1
	text = page.text()
	wikitext = mwparserfromhell.parse(text)
	for template in wikitext.filter_templates(recursive=False):
		if template.name.strip() in tabs_templates:
			
			if template.name.matches('ExternalContent/Line'):
				if template.has('url'):
					if template.get('url').value.strip() in text:
						continue
				if template.has('date'):
	
	newtext = str(wikitext)
	if text != newtext:
		print('Saving page %s...' % page.name)
		page.save(newtext, summary=summary)
	else:
		print('Skipping page %s...' % page.name)