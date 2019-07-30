from log_into_wiki import *
import mwparserfromhell

site = login('me', 'cod-esports')  # Set wiki
summary = 'Add CCMT data to Infobox using CM_ prefix for params and LeagueIconKey'  # Set summary

limit = -1
startat_page = None
print(startat_page)
#startat_page = '2014 EU Challenger Series/Spring/Series 2'

param_list=['StandardName','TournamentLevel','IsQualifier','IsPlayoffs','IsOfficial','Year','League','OverviewPage']

param_keys = {}
for param in param_list:
	param_keys[param] = param

param_keys['League'] = 'StandardLeague'

result = site.api('cargoquery', tables = 'CCMTournaments',
				  fields=','.join(param_list),
				  limit="max")
pages = result['cargoquery']

param_list.pop()

passed_startat = False if startat_page else True
lmt = 0
for p in pages:
	page = site.pages[p['title']['OverviewPage']]
	if lmt == limit:
		break
	if startat_page and page.name == startat_page:
		passed_startat = True
	if not passed_startat:
		#print("Skipping page %s" % page.name)
		continue
	data = p['title']
	lmt += 1
	text = page.text()
	wikitext = mwparserfromhell.parse(text)
	for template in wikitext.filter_templates():
		if template.name.matches('Infobox Tournament'):
			if template.has('StandardName'):
				for param in param_list:
					if template.has(param_keys[param]):
						template.get(param_keys[param]).name = 'CM_' + param_keys[param]
			for param in param_list:
				template.add('CM_' + param_keys[param], data[param])
			template.add('CM_LeagueIconKey', data['League'])
			if template.has('League'):
				template.remove('League')
	
	newtext = str(wikitext)
	if text != newtext:
		print('Saving page %s...' % page.name)
		page.save(newtext, summary=summary)
	else:
		print('Skipping page %s...' % page.name)
