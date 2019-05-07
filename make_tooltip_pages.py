from log_into_wiki import *
import mwparserfromhell, time

site = login('bot', 'lol')  # Set wiki
summary = 'Bot Edit'  # Set summary

limit = -1
startat_page = 'CompLexity.Black'
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
	if lmt < startat:
		print("Skipping page %s" % page.name)
	elif page.namespace == 0:
		try:
			newpage = site.pages['Tooltip:%s' % page.name]
			print('Saving page %s...' % newpage.name)
			newpage.save('{{RosterTooltip}}', summary = summary)
		except Exception as e:
			time.sleep(10)
			site = login('bot', 'lol')
			newpage = site.pages['Tooltip:%s' % page.name]
			print('Saving page %s...' % newpage.name)
			newpage.save('{{RosterTooltip}}', summary=summary)