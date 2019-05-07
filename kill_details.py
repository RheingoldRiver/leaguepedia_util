from log_into_wiki import *
import mwparserfromhell

site = login('me', 'lol')  # Set wiki
summary = 'kill details'  # Set summary

limit = -1
# startat_page = 'asdf'
this_template = site.pages['Template:TEMPLATE']  # Set template
pages = this_template.embeddedin()

lmt = 0
for page in [site.pages['International Wildcard All-Star Melbourne 2015']]:
	if lmt == limit:
		break
	lmt += 1
	if lmt < limit:
		print("Skipping page %s" % page.name)
	else:
		text = page.text()
		wikitext = mwparserfromhell.parse(text)
		for template in wikitext.filter_templates():
			if template.name.matches('MatchMaps2'):
				if template.has('details'):
					template.remove('details')
		
		newtext = str(wikitext)
		if text != newtext:
			print('Saving page %s...' % page.name)
			page.save(newtext, summary=summary)
		else:
			print('Skipping page %s...' % page.name)