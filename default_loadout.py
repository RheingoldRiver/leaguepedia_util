from log_into_wiki import *

loadout = login('me', 'default-loadout-esports')  # Set wiki
target = login('me', 'teamfighttactics')
summary = 'Default import of pages'  # Set summary

startat_namespace = None
print(startat_namespace)
startat_namespace = 10012

startat_comparison = startat_namespace - 1 if startat_namespace else -1

for ns in loadout.namespaces:
	print(ns)
	if ns > startat_comparison and ns != 4: # ns 4 is Project ns
		for page in loadout.allpages(namespace=ns):
			if target.pages[page.name].text() == '':
				target.pages[page.name].save(page.text(), summary=summary)
