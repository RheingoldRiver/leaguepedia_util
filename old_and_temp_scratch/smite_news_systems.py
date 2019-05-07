from log_into_wiki import *
import mwparserfromhell

site = login('me','smite-esports')
summary = 'Attempting to split news regions'
console_regions = [ 'nax', 'eux' ]

region_lookup = {
	'nax' : 'na',
	'eux' : 'eu'
}

limit = -1
#startat_player = 'asdf'
infobox = site.pages['Template:News Navbox']
pages = infobox.embeddedin()

pages_var = list(pages)

pages_array = [p.name for p in pages_var]

try:
	startat = pages_array.index(startat_player)
except NameError as e:
	startat = -1
print(startat)

lmt = 0
for page in pages_var:
	if lmt == limit:
		break
	lmt += 1
	if lmt < startat:
		print("Skipping page %s" % page.name)
	else:
		text = page.text()
		wikitext = mwparserfromhell.parse(text)
		for template in wikitext.filter_templates():
			if template.name.matches('NewsTeam') or template.name.matches('NewsTournament'):
				if template.has('region'):
					region = template.get('region').value.strip().lower()
					if region in console_regions:
						template.add('region', region_lookup[region])
						template.add('system','xbox')
					elif not template.has('system'):
						template.add('system','pc')
		newtext = str(wikitext)
		if text != newtext:
			print('Saving page %s...' % page.name)
			page.save(newtext, summary=summary)
		else:
			print('Skipping page %s (no changes)...' % page.name)