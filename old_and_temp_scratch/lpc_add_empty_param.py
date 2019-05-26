from log_into_wiki import *
import mwparserfromhell

site = login('bot','lol') # Set wiki
summary = 'Add empty param to LPC/End' # Set summary

limit = -1
startat_page = None
print(startat_page)
startat_page = 'Coliseo Dragons'
this_template = site.pages['Template:listplayer/Current/End'] # Set template
pages = this_template.embeddedin()

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
		if template.name.matches('listplayer/Current/End'):
			template.add(1,'')
			#template.remove(1, keep_field=True)
	
	newtext = str(wikitext)
	if text != newtext:
		print('Saving page %s...' % page.name)
		page.save(newtext, summary=summary)
	else:
		print('Skipping page %s...' % page.name)