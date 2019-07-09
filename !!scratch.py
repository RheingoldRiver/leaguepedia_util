from log_into_wiki import *
import mwparserfromhell

site = login('bot', 'lol')  # Set wiki
summary = 'Move initialorder before team1'  # Set summary

limit = -1
startat_page = None
print(startat_page)
startat_page = 'Data:LCS/2019 Season/Summer Season'
this_template = site.pages['Template:MatchSchedule']  # Set template
pages = this_template.embeddedin()

# with open('pages.txt', encoding="utf-8") as f:
# 	pages = f.readlines()

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
		if tl_matches(template, ['MatchSchedule']):
			if template.has('initialorder'):
				o = template.get('initialorder').value.strip()
				template.remove('initialorder')
				template.add('initialorder', o, before = 'team1')
	
	newtext = str(wikitext)
	if text != newtext:
		print('Saving page %s...' % page.name)
		page.save(newtext, summary=summary)
	else:
		print('Skipping page %s...' % page.name)
