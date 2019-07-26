from log_into_wiki import *

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

def blank_edit_pages(site, ls):
	for name in ls:
		p = site.pages[name]
		p.save(p.text(), summary='blank editing')

for wiki in wikis:
	site = login('me',wiki)
	
	blank_edit_pages(site, to_blank_edit)
	if wiki in to_blank_edits.keys():
		blank_edit_pages(site, to_blank_edits[wiki])
	
	for name in to_purges[wiki]:
		site.pages[name].purge()
	
	result = site.api('expandtemplates', format='json',
					prop = 'wikitext',
					text = '{{Project:Template/Current Tournaments Section}}'
	)
	
	text = result['expandtemplates']['wikitext']
	
	p2 = site.pages['Project:Current Tournaments Section']
	p2.save(text, summary = 'Automatically updating Current Tournaments',tags='daily_errorfix')
