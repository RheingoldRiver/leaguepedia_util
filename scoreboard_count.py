from log_into_wiki import *
import mwparserfromhell

site = login('me','lol') # Set wiki
summary = 'Bot Edit' # Set summary

limit = -1
startat_page = None
print(startat_page)
#startat_page = 'asdf'
this_template = site.pages['Module:Scoreboard'] # Set template
pages = this_template.embeddedin()

passed_startat = False if startat_page else True
lmt = 0
running_total = 0
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
	count_sb = text.count('Scoreboard/Season')
	count_mr = text.count('MatchRecapS8|')
	count = count_mr + count_sb
	running_total = running_total + count
	print('On page {}, count: {}, total: {}'.format(page.name, count, running_total))