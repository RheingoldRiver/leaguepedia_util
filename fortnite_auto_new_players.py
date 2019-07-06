from log_into_wiki import *
import mwparserfromhell
limit = -1

site = login('me', 'fortnite-esports')
summary = 'Automatically create player pages for Power Rankings'

result = site.api('cargoquery',
				  tables = 'TournamentResults=TR,TournamentResults__RosterLinks=RL,PlayerRedirects=PR',
				  join_on = 'TR._ID=RL._rowID,RL._value=PR.AllName',
				  where = 'RL._value IS NOT NULL AND PR._pageName IS NULL AND TR.PRPoints > "0"',
				  fields = 'RL._value=name',
				  group_by = 'RL._value',
				  limit = 'max'
				  )
default_text = site.pages['Help:Player Template'].text()
default_text = default_text.replace('<noinclude>','').replace('</noinclude>','').strip()

wikitext = mwparserfromhell.parse(default_text)
this_template = None
for template in wikitext.filter_templates():
	if template.name.matches('Infobox Player'):
		this_template = template
		this_template.add('pronly','Yes')
		break

lmt = 0
for item in result['cargoquery']:
	if lmt == limit:
		break
	lmt = lmt + 1
	name = item['title']['name']
	print(name)
	this_template.add('id', name)
	text = str(wikitext)
	site.pages[name].save(text, summary=summary)
