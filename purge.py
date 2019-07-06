from log_into_wiki import *
import mwparserfromhell

site = login('bot', 'fortnite-esports')  # Set wiki
summary = 'Forcing blank edit'  # Set summary

limit = -1
startat_page = None
print(startat_page)
# startat_page = 'Duji'
this_template = site.pages['Template:Infobox Player']  # Set template
pages = this_template.embeddedin()

# pages = site.categories['Pages with script errors']

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
	text = page.text()
	print('Purging page %s...' % page.name)
	site.api('purge', format='json',
			 titles = page.name,
			 forcelinkupdate = '1'
				 )
