from log_into_wiki import *
import mwparserfromhell

site = login('me', 'help')  # Set wiki
summary = 'jk interpreted |gp= |default= wrong the first time'  # Set summary

limit = -1
startat_page = None
print(startat_page)
# startat_page = 'asdf'
this_template = site.pages['Template:/row']  # Set template
pages = this_template.embeddedin()

# with open('pages.txt', encoding="utf-8") as f:
# 	pages = f.readlines()

pages = [site.pages['Extensions']]

def make_page(page, template):
	infobox = mwparserfromhell.nodes.Template('Extension infobox')
	infobox.add('name', template.get(1).value.strip())
	if template.has(2):
		infobox.add('desc', template.get(2).value.strip())
	if template.has('link'):
		infobox.add('link', '[[%s|MediaWiki.org]]' % template.get('link').value.strip())
	page.save(str(infobox), summary = 'populating data based on Extensions page, blame any mistakes on pcj using unnamed args')

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
		if tl_matches(template, ['/row']):
			extension = template.get(1).value.strip()
			extension_page = site.pages['Extension:' + extension]
			extension_text = extension_page.text()
			if extension_text == '':
				make_page(extension_page, template)
				continue
			extension_wikitext = mwparserfromhell.parse(extension_text)
			for tl in extension_wikitext.filter_templates():
				print(tl.name)
				if tl.name.matches('Extension infobox'):
					if template.has('gp'):
						tl.add('gp', 'yes')
					if template.has('default'):
						tl.add('default', 'yes')
			print(extension)
			if str(extension_wikitext) != extension_text:
				extension_page.save(str(extension_wikitext), summary=summary)
					
	
	newtext = str(wikitext)
	if text != newtext:
		print('Saving page %s...' % page.name)
		page.save(newtext, summary=summary)
	else:
		print('Skipping page %s...' % page.name)
