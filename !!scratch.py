from log_into_wiki import *
import mwparserfromhell

site = login('me', 'lol')  # Set wiki
summary = 'Bot Edit'  # Set summary

limit = -1
startat_page = None
print(startat_page)
# startat_page = 'asdf'
this_template = site.pages['Template:TEMPLATE']  # Set template
pages = this_template.embeddedin()

# with open('pages.txt', encoding="utf-8") as f:
# 	pages = f.readlines()

params = {
	1: 'player',
	2: 'country',
	3: 'name',
	4: 'role',
	'res': 'residency',
	'joined': 'joined',
	'contract': 'contract',
	'rejoined': 'rejoined',
}

pages = [ site.pages['Team SoloMid'] ]

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
		if tl_matches(template, ['Listplayer/Current']):
			template.name = 'TeamMember'
			for key in params.keys():
				if template.has(key):
					val = template.get(key).value.strip()
					template.remove(key)
					template.add(params[key], val)
			print(str(template))
