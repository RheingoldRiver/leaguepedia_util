from log_into_wiki import *
import mwparserfromhell
summary = 'auto updating residency to PCS'
with open('pages.txt', encoding='utf-8') as f:
	titles = f.readlines()

titles = [_.strip() for _ in titles]

site = login('bot', 'lol')

for title in titles:
	page = site.pages[title]
	text = page.text()
	wikitext = mwparserfromhell.parse(text)
	for template in wikitext.filter_templates():
		if tl_matches(template, ['Infobox Player']):
			if template.get('isretired').value.strip() == 'Yes':
				continue
			old_res = template.get('residency').value.strip()
			template.add('residency', 'PCS')
			template.add('checkbox-res', 'Yes')
			template.add('residency-prev1', old_res)
	newtext = str(wikitext)
	if text != newtext:
		print('Saving page %s...' % page.name)
		page.save(newtext, summary=summary)
	else:
		print('Skipping page %s...' % page.name)
