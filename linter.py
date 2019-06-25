from log_into_wiki import *
import mwparserfromhell

site = login('me', 'lol')  # Set wiki
summary = 'Adding linting error category (mismatched divs)'  # Set summary

limit = -1
startat_page = None
print(startat_page)
startat_page = '2014 LNL Spring Qualifiers/Hong Kong and Macau'
this_template = site.pages['Template:Infobox Tournament']  # Set template
pages = this_template.embeddedin()

pages = [site.pages['Lega Prima/Season 1']]

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
	if page.namespace != 0:
		continue
	lmt += 1
	parsed_text = site.expandtemplates('{{:' + page.name + '}}', title="Main Page")
	if parsed_text.count('<div') != parsed_text.count('</div>'):
		print('Saving page %s...' % page.name)
		page.save(page.text() + '[[Category:Pages With Mismatched Divs]]', summary = summary)
	else:
		print('Skipping page %s...' % page.name)