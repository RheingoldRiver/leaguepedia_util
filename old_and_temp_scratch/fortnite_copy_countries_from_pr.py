from log_into_wiki import *
import mwparserfromhell

site = login('bot', 'fortnite-esports')  # Set wiki
summary = 'Guess country from PR table'  # Set summary

limit = -1
startat_page = None
print(startat_page)
startat_page = '12AM Poppin'
# this_template = site.pages['Template:TEMPLATE']  # Set template
# pages = this_template.embeddedin()
c = site.categories['Power Ranking Player Pages']

# with open('pages.txt', encoding="utf-8") as f:
# 	pages = f.readlines()

passed_startat = False if startat_page else True
lmt = 0
for page in c:
	if lmt == limit:
		break
	if startat_page and page.name == startat_page:
		passed_startat = True
	if not passed_startat:
		print("Skipping page %s" % page.name)
		continue
	lmt += 1
	text = page.text()
	response = site.api('cargoquery',
						tables = 'PowerRankings',
						fields = 'Country',
						where = 'Player = "%s"' % page.name
						)
	result = response['cargoquery']
	country = None
	if len(result) > 0:
		country = result[0]['title']['Country']
	wikitext = mwparserfromhell.parse(text)
	if country:
		for template in wikitext.filter_templates():
			if tl_matches(template, ['Infobox Player']):
				template.add('country', country)
				continue
	
	newtext = str(wikitext)
	if text != newtext:
		print('Saving page %s...' % page.name)
		page.save(newtext, summary=summary)
	else:
		print('Skipping page %s...' % page.name)
