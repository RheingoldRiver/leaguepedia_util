from log_into_wiki import *
import mwparserfromhell

site = login('bot', 'lol')  # Set wiki
summary = 'new feature yay'  # Set summary

limit = -1
startat_page = 'DS Gaming'
this_template = site.pages['Template:Infobox Team']  # Set template
pages = this_template.embeddedin()

pages_var = list(pages)

pages_array = [p.name for p in pages_var]

try:
	startat = pages_array.index(startat_page)
except NameError as e:
	startat = -1
except ValueError as e:
	startat = -1
print(startat)

lmt = 0
for page in pages_var:
	if lmt == limit:
		break
	lmt += 1
	if lmt < startat or page.namespace != 0:
		print("Skipping page %s" % page.name)
	else:
		newpage = site.pages[page.name + '/Schedule History']
		text = '{{TeamTabsHeader}}\n{{TeamScheduleHistory}}'
		print('Saving page %s' % newpage.name)
		newpage.save(text, summary = summary)