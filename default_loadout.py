import time

from river_mwclient.esports_client import EsportsClient
from river_mwclient.auth_credentials import AuthCredentials
from mwclient.errors import AssertUserFailedError

credentials = AuthCredentials(user_file="me")
loadout = EsportsClient('default-loadout') #  set wiki
target = EsportsClient('legendsofruneterra-esports', credentials=credentials) #  set wiki
summary = 'Default loadout of pages'  # Set summary

startat_namespace = None
print(startat_namespace)
startat_namespace = 0

startat_page = None
print(startat_page)
# startat_page = 'Module:Navbox/Aether II/en'

overwrite_existing = True

startat_comparison = -1 if startat_namespace is None else startat_namespace - 1

passed_startat = False

for ns in loadout.client.namespaces:
	print(ns)
	if ns > startat_comparison: # ns 4 is Project ns
		for page in loadout.client.allpages(namespace=ns):
			# time.sleep(1)
			print(page.name)
			new_title = page.name
			if ns == 4:
				new_title = 'Project:{}'.format(page.page_title)
			if startat_page == page.name:
				passed_startat = True
			if startat_page and not passed_startat:
				continue
			if overwrite_existing or not target.client.pages[new_title].exists:
				try:
					target.client.pages[new_title].save(page.text(), summary=summary)
				except AssertUserFailedError:
					target.login()
					target.client.pages[new_title].save(page.text(), summary=summary)
