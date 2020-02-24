from river_mwclient.esports_site import EsportsSite

site = EsportsSite('lol')'siege-esports')

limit = -1
startat_player = 'asdf'
infobox = site.client.pages['Template:Infobox Team']
pages = infobox.embeddedin()

pages_var = list(pages)

pages_array = [p.name for p in pages_var]

try:
	startat = pages_array.index(startat_player)
except ValueError as e:
	startat = -1
print(startat)

lmt = 0
for page in pages_var:
	if lmt == limit:
		break
	lmt += 1
	if lmt < startat:
		print("Skipping page %s" % page.name)
	else:
		if page.namespace == 0:
			print("Saving page: " + page.name)
			site.client.pages[page.name + '/Schedule'].save(
				'{{TeamTabsHeader}}\n{{TeamSchedule|%s}}' % page.name)
