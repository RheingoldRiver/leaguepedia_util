from log_into_wiki import *
limit = -1
site = login('bot','lol')
t = site.pages["Template:Item Page"]

pages = t.embeddedin()

c = site.categories['Pages with script errors']

lmt = 0
for p in c:
#for p in pages:
	if lmt == limit:
		break
	lmt += 1
	print(p.name)
	text = p.text()
	p.save(text,'blank editing')
