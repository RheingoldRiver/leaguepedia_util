from log_into_wiki import *

site = login('me','lol')

to_blank_edit = ['Project:Top Schedule', 'Project:Matches Section/Matches',
				 'Project:Matches Section/Results']

for name in to_blank_edit:
	p = site.pages[name]
	p.save(p.text(), summary='blank editing')


result = site.api('expandtemplates', format='json',
				prop = 'wikitext',
				text = '{{Project:Template/Current Tournaments Section}}'
)

text = result['expandtemplates']['wikitext']

p2 = site.pages['Project:Current Tournaments Section']
p2.save(text, summary = 'Automatically updating Current Tournaments',tags='daily_errorfix')

p3 = site.pages('League of Legends Esports Wiki')

p3.purge()

p4 = site.pages('Match History Index')

p4.purge()