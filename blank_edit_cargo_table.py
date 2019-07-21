from log_into_wiki import *
limit = -1
site = login('bot','lol')

response = site.api('cargoquery', tables = 'Champions', fields='_pageName=Page',
					group_by = '_pageName', limit='max'
					)
pages = []
for r in response['cargoquery']:
	pages.append(r['title']['Page'])
print(pages)

lmt = 0
#for p in c:
#for p in pages:
for page in pages:
	if lmt == limit:
		break
	p = site.pages[page]
	lmt += 1
	print(p.name)
	text = p.text()
	p.save(text,'blank editing')
