from river_mwclient.esports_site import EsportsSite
import mwparserfromhell

site = EsportsSite('lol')'lol') # Set wiki
summary = 'Bot Edit' # Set summary


for namespace in site.namespaces:
	if namespace < 1:
		continue
	page = site.client.pages['MediaWiki:Editnotice-' + str(namespace)]
	page.save('{{int:Editnotice-0}}', summary = "Creating char insert page")
