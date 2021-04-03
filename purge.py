import time

from mwrogue.esports_client import EsportsClient
from mwcleric.auth_credentials import AuthCredentials

credentials = AuthCredentials(user_file="me")
site = EsportsClient('lol', credentials=credentials) # Set wiki
summary = 'Forcing blank edit'  # Set summary

limit = -1
startat_page = None
print(startat_page)
startat_page = 'EShen'
this_template = site.client.pages['Template:Infobox Player']  # Set template
pages = this_template.embeddedin()

# pages = site.client.categories['Pages with script errors']

passed_startat = False if startat_page else True
lmt = 0
for page in pages:
	if lmt == limit:
		break
	if startat_page and page.name == startat_page:
		passed_startat = True
	if not passed_startat:
		print("Skipping page %s" % page.name)
		continue
	print('Purging page %s...' % page.name)
	site.purge(page)
