from log_into_wiki import *

loadout = login('me', 'default-loadout-esports')  # Set wiki
target = login('me', 'teamfighttactics')
summary = 'Default import of pages'  # Set summary


for ns in loadout.namespaces:
	print(ns)
	if ns > -1:
		for page in loadout.allpages(namespace=ns):
			if target.pages[page.name].text() == '':
				target.pages[page.name].save(page.text(), summary=summary)
