from river_mwclient.esports_client import EsportsClient
from river_mwclient.auth_credentials import AuthCredentials

credentials = AuthCredentials(user_file="me")
loadout = EsportsClient('lol', credentials=credentials) #  set wiki
target = EsportsClient('splatoon2', credentials=credentials) #  set wiki
summary = 'Backing up spyro'  # Set summary

startat_namespace = None
print(startat_namespace)
startat_namespace = 274

startat_page = None
print(startat_page)
startat_page = 'Module:Navbox/Aether II/en'

startat_comparison = startat_namespace - 1 if startat_namespace else -1

passed_startat = False

for ns in loadout.client.namespaces:
	print(ns)
	if ns > startat_comparison and ns != 4: # ns 4 is Project ns
		for page in loadout.client.allpages(namespace=ns):
			if startat_page == page.name:
				passed_startat = True
			if startat_page and not passed_startat:
				continue
			if target.client.pages[page.name].text() == '':
				target.client.pages[page.name].save(page.text(), summary=summary)
