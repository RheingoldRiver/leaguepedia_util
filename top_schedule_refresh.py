from river_mwclient.esports_site import EsportsSite

wikis = [ 'lol', 'cod-esports' ]

to_purges = {
	'lol' : ['League of Legends Esports Wiki', 'Match History Index'],
	'cod-esports' : ['Call of Duty Esports Wiki']
}

to_blank_edit = ['Project:Top Schedule', 'Project:Matches Section/Matches',
					 'Project:Matches Section/Results']

to_blank_edits = {
	'lol' : ['Project:Korizon Standings']
}

def blank_edit_pages(site: EsportsSite, ls):
	for name in ls:
		p = site.client.pages[name]
		p.save(p.text(), summary='blank editing')

for wiki in wikis:
	site = EsportsSite(wiki, user_file='me')
	
	blank_edit_pages(site, to_blank_edit)
	if wiki in to_blank_edits.keys():
		blank_edit_pages(site, to_blank_edits[wiki])
	
	for name in to_purges[wiki]:
		site.client.pages[name].purge()
	
	result = site.client.api('expandtemplates', format='json',
					prop = 'wikitext',
					text = '{{Project:Template/Current Tournaments Section}}'
	)
	
	text = result['expandtemplates']['wikitext']
	
	p2 = site.client.pages['Project:Current Tournaments Section']
	p2.save(text, summary = 'Automatically updating Current Tournaments',tags='daily_errorfix')
