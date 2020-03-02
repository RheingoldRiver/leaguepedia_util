from river_mwclient.esports_client import EsportsClient
from river_mwclient.auth_credentials import AuthCredentials

credentials = AuthCredentials(user_file="me")
archive = EsportsClient('lol-archive', credentials=credentials) #  set wiki
live = EsportsClient('lol', credentials=credentials) #  set wiki

pages = []

for page in archive.client.allpages(namespace=0):
	pages.append((page.name, live.pages[page.name].exists))

text = []

for p in pages:
	text.append('{}\t{}'.format(p[0], str(p[1])))

with open('archive_pages.txt', 'w+', encoding="utf-8") as f:
	f.write('\n'.join(text))
