import datetime
from time import mktime

from log_into_wiki import *

loadout = login('me', 'spyro')  # Set wiki
target = login('me', 'wikisandbox')
summary = 'Backing up spyro'  # Set summary

startat_namespace = None
print(startat_namespace)
startat_namespace = 274

startat_page = None
print(startat_page)
startat_page = 'Module:Navbox/Aether II/en'

startat_comparison = startat_namespace - 1 if startat_namespace else -1

passed_startat = False

for ns in loadout.namespaces:
	print(ns)
	if ns > startat_comparison and ns != 4: # ns 4 is Project ns
		for page in loadout.allpages(namespace=ns):
			if startat_page == page.name:
				passed_startat = True
			if startat_page and not passed_startat:
				continue
			if target.pages[page.name].text() == '':
				target.pages[page.name].save(page.text(), summary=summary)
