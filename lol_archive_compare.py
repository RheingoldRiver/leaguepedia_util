from river_mwclient.esports_site import EsportsSite

archive = EsportsSite('lol-archive', user_file="me") # Set wiki
live = EsportsSite('lol', user_file="me") # Set wiki

pages = []

for page in archive.client.allpages(namespace=0):
	pages.append((page.name, live.pages[page.name].exists))

text = []

for p in pages:
	text.append('{}\t{}'.format(p[0], str(p[1])))

with open('archive_pages.txt', 'w+', encoding="utf-8") as f:
	f.write('\n'.join(text))
