from log_into_wiki import *
import mwparserfromhell

site = login('me','lol') # Set wiki
summary = 'Bot Edit' # Set summary


for namespace in site.namespaces:
	if namespace < 1:
		continue
	page = site.pages['MediaWiki:Editnotice-' + str(namespace)]
	page.save('{{int:Editnotice-0}}', summary = "Creating char insert page")
