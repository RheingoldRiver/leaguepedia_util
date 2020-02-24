from river_mwclient.esports_site import EsportsSite
limit = -1
site = login('bot','lol')
t = site.client.pages["Template:Item Page"]

pages = t.embeddedin()

cat = 'Brackets With Conflicting Field Errors'
c = site.categories[cat]

lmt = 0
for p in c:
#for p in pages:
	if lmt == limit:
		break
	lmt += 1
	print(p.name)
	text = p.text()
	newtext = text.replace('\n[[Category:' + cat + ']]','')
	p.save(newtext,"this category was a mistake")
