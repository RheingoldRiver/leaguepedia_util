from river_mwclient.esports_site import EsportsSite
import mwparserfromhell

site = EsportsSite('lol', user_file="me") # Set wiki
summary = 'Bot Edit' # Set summary

limit = -1
startat_page = None
print(startat_page)
#startat_page = 'asdf'
this_template = site.client.pages['Template:TEMPLATE'] # Set template
pages = this_template.embeddedin()

# with open('pages.txt', encoding="utf-8") as f:
# 	pages = f.readlines()

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
	lmt += 1
	text = page.text()
	wikitext = mwparserfromhell.parse(text)
	for template in wikitext.filter_templates():
		if template.name.matches(['TEMPLATEYOUCAREABOUT']):
			print(template) # here so it doesn't think there's an error
			# TODO
	
	newtext = str(wikitext)
	if text != newtext:
		print('Saving page %s...' % page.name)
		page.save(newtext, summary=summary)
	else:
		print('Skipping page %s...' % page.name)
