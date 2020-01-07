from log_into_wiki import *
import mwparserfromhell, time
limit = -1

site = login('bot', 'fortnite-esports')
summary = 'Automatically create player pages for Power Rankings'

result = site.api('cargoquery',
				  tables = 'TournamentResults=TR,TournamentResults__RosterLinks=RL,_pageData=PD,Tournaments=T',
				  join_on = 'TR._ID=RL._rowID,RL._value=PD._pageName,TR.OverviewPage=T._pageName',
				  where = 'PD._pageName IS NULL AND RL._value IS NOT NULL AND TR.PRPoints > "0"',
				  fields = 'RL._value=name,T.Region=res',
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
	res = item['title']['res']
	if name == '0':
		continue
	try:
		page = site.pages[name]
		if page.text() != '':
			print('Page %s already exists, skipping' % name)
			page.save(page.text())
			continue
		print('Processing page %s...' % name)
		this_template.add('residency', res)
		this_template.add('id', name)
		text = str(wikitext)
		page.save(text, summary=summary)
	except Exception as e:
		time.sleep(10)
		site.pages['User:RheingoldRiver/auto players errors'].save(e)
