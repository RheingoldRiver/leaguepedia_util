from log_into_wiki import *
import mwparserfromhell

site = login('bot', 'lol')  # Set wiki
summary = 'remove all extra mhp params/text'  # Set summary

limit = -1
startat_page = None
print(startat_page)
startat_page = 'Cop/Match History'
this_template = site.pages['Template:MatchHistoryPlayer']  # Set template
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
	newtext = '{{PlayerTabsHeader}}\n{{MatchHistoryPlayer}}'
	if text != newtext:
		print('Saving page %s...' % page.name)
		page.save(newtext, summary=summary)
	else:
		print('Skipping page %s...' % page.name)