from log_into_wiki import *
import mwparserfromhell

site = login('me','lol') # Set wiki
summary = 'add leaving classes' # Set summary

limit = -1
#startat_page = 'asdf'
this_template = site.pages['Template:PortalCurrentRosters'] # Set template
pages = this_template.embeddedin()

pages_var = list(pages)

pages_array = [p.name for p in pages_var]

try:
	startat = pages_array.index(startat_page)
except NameError as e:
	startat = -1
except ValueError as e:
	startat = -1
print(startat)

lmt = 0
for page in pages_var:
	if lmt == limit:
		break
	lmt += 1
	if lmt < startat:
		print("Skipping page %s" % page.name)
		continue
	if '2019' not in page.name or 'Midseason' not in page.name:
		print("Skipping page %s" % page.name)
		continue
	text = page.text()
	wikitext = mwparserfromhell.parse(text)
	for template in wikitext.filter_templates():
		if template.name.matches('PortalCurrentRosters'):
			for role in ['t', 'j', 'm', 'a', 's', 'c']:
				key = role + '_old_classes'
				role_key = role + '_old'
				if not template.has(key) and template.has(role_key):
					template.add(key, 'leave', before=role_key)
	
	newtext = str(wikitext)
	if text != newtext:
		print('Saving page %s...' % page.name)
		page.save(newtext, summary=summary)
	else:
		print('Skipping page %s...' % page.name)