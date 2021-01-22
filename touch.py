from river_mwclient.esports_client import EsportsClient
from river_mwclient.auth_credentials import AuthCredentials
import time
limit = -1
credentials = AuthCredentials(user_file="me")
site = EsportsClient('fortnite', credentials=credentials) # Set wiki


pages = site.pages_using('Infobox Player')

# c = site.client.categories['Pages with script errors']

startat_page = None
passed_startat = True

lmt = 0
#for p in c:
for p in pages:
	if lmt == limit:
		break
	if p.name == startat_page:
		passed_startat = True
	if not passed_startat:
		continue
	lmt += 1
	print(p.name)
	site.touch(p)
