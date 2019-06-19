from log_into_wiki import *

site = login('me','lol')

to_blank_edit = ['Project:Top Schedule', 'Project:Matches Section/Matches',
				 'Project:Matches Section/Results', 'Project:Korizon Standings']

to_purge = ['League of Legends Esports Wiki', 'Match History Index']

for name in to_blank_edit:
	p = site.pages[name]
	p.save(p.text(), summary='blank editing')

for name in to_purge:
	site.pages[name].purge()

result = site.api('expandtemplates', format='json',
				prop = 'wikitext',
				text = '{{Project:Template/Current Tournaments Section}}'
)

text = result['expandtemplates']['wikitext']

p2 = site.pages['Project:Current Tournaments Section']
p2.save(text, summary = 'Automatically updating Current Tournaments',tags='daily_errorfix')