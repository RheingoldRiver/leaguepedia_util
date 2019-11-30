from log_into_wiki import *
import mwparserfromhell

site = login('bot', 'lol')  # Set wiki
summary = 'Add language/date'  # Set summary

limit = -1
startat_page = None
print(startat_page)
# startat_page = 'asdf'
this_template = site.pages['Template:PlayerPronunciationFile']  # Set template
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
		if tl_matches(template, ['PlayerPronunciationFile']):
			recordedby = template.get('recordedby').value.strip()
			if recordedby == 'Daedalus':
				template.add('date', '2019-08-14')
				if 'English' in page.name:
					template.add('language', 'English')
				else:
					template.add('language', 'Danish')
			elif recordedby == 'Raafaa':
				template.add('language', 'English')
				template.add('date', '2019-08-22')
			elif recordedby == 'Click':
				template.add('language', 'Russian')
				template.add('date', '2019-11-21')
			elif recordedby == 'theaspectoftwilight':
				template.add('language', 'Spanish')
				template.add('date', '2019-10-03')
			elif recordedby == 'katsudion':
				template.add('language', 'Japanese')
				template.add('date', '2019-11-21')
			elif recordedby == 'Grindelwald':
				template.add('language', 'Vietnamese')
				template.add('date', '2019-08-07')
			elif recordedby == 'Elmyra':
				template.add('date', '2019-10-05')
	
	newtext = str(wikitext)
	if text != newtext:
		print('Saving page %s...' % page.name)
		page.save(newtext, summary=summary)
	else:
		print('Skipping page %s...' % page.name)
