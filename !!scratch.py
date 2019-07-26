from log_into_wiki import *
limit = -1
site = login('me','lol')
t = site.pages["Template:Item Page"]

pages = t.embeddedin()

c = site.categories['Casters']

lmt = 0
for p in c:
	if lmt == limit:
		break
	lmt += 1
	new_page = site.pages[p.name + '/Casting History']
	new_page.save('{{PlayerTabsHeader}}\n{{CastingHistory}}', 'Creating Casting History Pages')
