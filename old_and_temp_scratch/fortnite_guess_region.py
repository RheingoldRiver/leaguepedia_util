from log_into_wiki import *
import mwparserfromhell
limit = -1

site = login('bot', 'fortnite-esports')
summary = 'Guess region if possible'
startat_page = 'Ch1psonbae'

lmt = 0
passed_startat = False if startat_page else True
for page in site.categories['Power Ranking Player Pages']:
	if lmt == limit:
		break
	if startat_page and page.name == startat_page:
		passed_startat = True
	if not passed_startat:
		print("Skipping page %s" % page.name)
		continue
	lmt += 1
	name = page.name
	print('starting page %s...' % page.name)
	response = site.api('cargoquery',
					  tables = 'Tournaments=T,TournamentResults=TR,TournamentResults__RosterLinks=RL,PlayerRedirects=PR',
					  join_on='T._pageName=TR.OverviewPage,TR._ID=RL._rowID,RL._value=PR.AllName',
					  where = 'PR._pageName="%s"' % name,
					  fields = 'T.Region',
					  group_by = 'T.Region'
					  )
	result = response['cargoquery']
	if len(result) == 1:
		text = page.text()
		wikitext = mwparserfromhell.parse(text)
		for template in wikitext.filter_templates():
			if template.name.matches('Infobox Player'):
				template.add('residency', result[0]['title']['Region'])
		print('Saving page %s...' % page.name)
		page.save(str(wikitext), summary = summary)
