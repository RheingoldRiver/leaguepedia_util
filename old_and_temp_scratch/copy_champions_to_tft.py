from log_into_wiki import *
import mwparserfromhell

site = login('me', 'lol')  # Set wiki
tft = login('me', 'teamfighttactics')
summary = 'Initial Population of Champion Pages'  # Set summary

limit = -1
startat_page = None
print(startat_page)
# startat_page = 'asdf'
cat = site.categories['Champions']

passed_startat = False if startat_page else True
lmt = 0
for page in cat:
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
		if template.name.matches('Infobox Champion'):
			new_tl = mwparserfromhell.nodes.Template('Infobox Champion')
			new_tl.add('name', template.get('name').value.strip() + '\n')
			new_tl.add('title', template.get('title').value.strip())
			if template.has('realname'):
				new_tl.add('realname', template.get('realname').value.strip())
			new_tl.add('tier','')
			new_tl.add('origin', '')
			new_tl.add('class', '')
			new_tl.add('ability', '')
			tft.pages[page.name].save(str(new_tl), summary=summary)