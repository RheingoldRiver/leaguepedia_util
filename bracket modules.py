from log_into_wiki import *
import mwparserfromhell, re

site = login('me', 'lol')  # Set wiki
summary = 'Bot Edit'  # Set summary

limit = -1
# startat_page = 'asdf'
this_template = site.pages['Module:Bracket']  # Set template
pages = this_template.embeddedin(namespace='828')

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
	if lmt < startat:
		print("Skipping page %s" % page.name)
	else:
		p = page.name
		docpage = site.pages[p + '/doc']
		tooltippage = site.pages['Tooltip:' + p]
		text = page.text()
		newtext = text.replace('[[Category:Bracket Definitions]]','[[Category:Bracket Definitions|{{SubpageCategorySort}}]]')
		if text != newtext:
			print('Saving page %s...' % page.name)
			page.save(newtext, summary=summary)
		else:
			print('Skipping page %s...' % page.name)
		tooltippage.save('{{BracketTooltip}}')