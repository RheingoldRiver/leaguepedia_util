from log_into_wiki import *
import weekly_utils as util
import mwparserfromhell

site = login('bot', 'lol')  # Set wiki
summary = 'attempting social link fixes'  # Set summary

limit = -1
#startat_page = 'Enraged eSports'
this_template = site.pages['Template:Infobox Team']  # Set template
pages = this_template.embeddedin()

pages_var = list(pages)

pages_array = [p.name for p in pages_var]  # get the name of the page as a string instead of a page object

try:
	startat = pages_array.index(startat_page)
except NameError as e:
	startat = -1
print(startat)

lmt = 0
for page in pages_var:
	if lmt == limit:
		break
	lmt += 1
	if lmt < startat:
		print("Skipping page %s" % page.name)
	else:
		text = page.text()
		wikitext = mwparserfromhell.parse(text)
		for template in wikitext.filter_templates():
			if template.name.matches('Infobox Team') or template.name.matches('Infobox_Team'):
				util.fixInfoboxTeam(template)
		newtext = str(wikitext)
		newtext = newtext.replace('Infobox_Team','Infobox Team')
		if text != newtext:
			print('Saving page %s...' % page.name)
			page.save(newtext, summary=summary)
		else:
			print('Skipping page %s...' % page.name)