from log_into_wiki import *
import mwparserfromhell

site = login('bot','lol') # Set wiki
summary = 'Replacing with single cargo template' # Set summary

limit = -1
startat_page = None
print(startat_page)
#startat_page = 'asdf'
this_template = site.pages['Template:IPS'] # Set template
pages = this_template.embeddedin()

passed_startat = False if startat_page else True
lmt = 0
for page in pages:
	if lmt == limit:
		break
	if startat_page and page.name == startat_page:
		passed_startat = True
	if not passed_startat or not re.match(r'.*/.*/\d+', page.name):
		print("Skipping page %s" % page.name)
		continue
	lmt += 1
	print('Saving page %s...' % page.name)
	page.save('{{PlayerTabsHeader}}\n{{PlayerYearStats}}', summary = summary)