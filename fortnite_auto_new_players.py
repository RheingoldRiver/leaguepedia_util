from river_mwclient.esports_client import EsportsClient
from river_mwclient.auth_credentials import AuthCredentials
import mwparserfromhell, time
limit = -1

credentials = AuthCredentials(user_file="me")
site = EsportsClient('fortnite', credentials=credentials) #  set wiki
summary = 'Automatically create player pages for Power Rankings'

result = site.cargo_client.query(
				  tables = 'TournamentResults=TR,TournamentResults__RosterLinks=RL,_pageData=PD,Tournaments=T',
				  join_on = 'TR._ID=RL._rowID,RL._value=PD._pageName,TR.OverviewPage=T._pageName',
				  where = 'PD._pageName IS NULL AND RL._value IS NOT NULL AND TR.PRPoints > "0"',
				  fields = 'RL._value=name,T.Region=res',
				  group_by = 'RL._value',
				  limit = 'max'
				  )
default_text = site.client.pages['Help:Player Template'].text()
default_text = default_text.replace('<noinclude>','').replace('</noinclude>','').strip()

wikitext = mwparserfromhell.parse(default_text)
this_template = None
for template in wikitext.filter_templates():
	if template.name.matches('Infobox Player'):
		this_template = template
		this_template.add('pronly','Yes')
		break

lmt = 0
for item in result:
	if lmt == limit:
		break
	lmt = lmt + 1
	name = item['title']['name']
	res = item['title']['res']
	if name == '0':
		continue
	try:
		page = site.client.pages[name]
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
		site.client.pages['User:RheingoldRiver/auto players errors'].save(e)
