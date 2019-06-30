from log_into_wiki import *
import mwparserfromhell

site = login('me', 'fortnite-esports')  # Set wiki
summary = 'Add place to team roster'  # Set summary

limit = -1
startat_page = None
print(startat_page)
# startat_page = 'Fortnite World Cup 2019/NAE/Week 5'
this_template = site.pages['Template:TeamRoster']  # Set template
pages = this_template.embeddedin()

# with open('pages.txt', encoding="utf-8") as f:
# 	pages = f.readlines()

def make_lookup(overview):
	ret = {}
	data_text = site.pages['Data:' + overview.name].text()
	for template in mwparserfromhell.parse(data_text).filter_templates():
		if tl_matches(template, ['TournamentResults/Line']):
			if template.has('team') and template.has('place'):
				ret[template.get('team').value.strip()] = template.get('place').value.strip()
	return ret

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
	lookup = make_lookup(page)
	text = page.text()
	wikitext = mwparserfromhell.parse(text)
	for template in wikitext.filter_templates():
		if tl_matches(template, ['TeamRoster']):
			if template.has('team'):
				team = template.get('team').value.strip()
				if team in lookup:
					template.add('place', lookup[team])
	
	newtext = str(wikitext)
	if text != newtext:
		print('Saving page %s...' % page.name)
		page.save(newtext, summary=summary)
	else:
		print('Skipping page %s...' % page.name)
