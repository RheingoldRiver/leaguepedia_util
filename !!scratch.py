from log_into_wiki import *
import mwparserfromhell

site = login('me', 'lol')  # Set wiki
summary = '|sub=Yes |trainee=Yes & take out of |status='  # Set summary

limit = -1
startat_page = None
print(startat_page)
# startat_page = 'asdf'
this_template = site.pages['Template:RCInfo']  # Set template
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
		if tl_matches(template, ['RCInfo']):
			if template.has('status'):
				if template.get('status').value.strip().lower() == 'sub':
					template.add('sub', 'Yes')
					template.add('status', '')
				if template.get('status').value.strip().lower() == 'trainee':
					template.add('trainee', 'Yes')
					template.add('status', '')

	newtext = str(wikitext)
	if text != newtext:
		print('Saving page %s...' % page.name)
		page.save(newtext, summary=summary)
	else:
		print('Skipping page %s...' % page.name)
