from river_mwclient.esports_site import EsportsSite
import mwparserfromhell

find = 'prettytable'
replace = ' wikitable'

site = EsportsSite('lol') 'fortnite-esports')  # Set wiki
summary = 'Find-Replace: {} -> {}'.format(find, replace)  # Set summary

limit = -1
startat_page = None
print(startat_page)
# startat_page = 'asdf'
# this_template = site.client.pages['Template:TEMPLATE']  # Set template
# pages = this_template.embeddedin()

with open('pages.txt', encoding="utf-8") as f:
	pages = f.readlines()

passed_startat = False if startat_page else True
lmt = 0
for page in pages:
	page = page.strip()
	old_text = site.client.pages[page].text()
	new_text = old_text.replace(find, replace)
	site.client.pages[page].save(new_text, summary = summary)
