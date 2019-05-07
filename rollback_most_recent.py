from log_into_wiki import *
limit = -1

site = login('bot', 'lol')


with open('pages.txt', encoding="utf-8") as f:
	pages = f.readlines()
pages = [page.strip() for page in pages]

lmt = 0
for page in pages:
	if lmt == limit:
		break
	lmt += 1
	data = site.api('query',
		format = 'json',
		prop = 'revisions',
		titles = page,
		rvprop = 'content',
		rvlimit = '2'
	)
	datapages = data['query']['pages']
	text = ''
	print(page)
	for pg in datapages:
		print(pg)
		text = datapages[pg]['revisions'][1]['*']
	p = site.pages[page]
	p.save(text,'Reverting oops')