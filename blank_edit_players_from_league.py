from log_into_wiki import *
limit = -1
site = login('me','lol')

with open('pages.txt', encoding="utf-8") as f:
	tournaments = f.readlines()
	
pages = set()

for tournament in tournaments:
	response = site.api('cargoquery',
		tables = 'ScoreboardPlayer',
		where = 'OverviewPage="%s"' % tournament.strip().replace('_', ' '),
		fields = 'Link',
		group_by = 'Link'
	)
	for item in response['cargoquery']:
		pages.add(item['title']['Link'])

lmt = 0
for page in pages:
	if lmt == limit:
		break
	p = site.pages[page]
	lmt += 1
	print(p.name)
	text = p.text()
	if text != '':
		p.save(text,'blank editing')
