from log_into_wiki import *
import mwparserfromhell

site = login('me','lol') # Set wiki
summary = 'flag to player template' # Set summary

limit = -1
startat_page = None
print(startat_page)
startat_page = '2015 Season China Regional Finals'
this_template = site.pages['Template:Flag'] # Set template
pages = this_template.embeddedin()

def fix_player(line):
	new_line =  re.sub(r'\\{\\{flag\\|(.+?)\\}\\}\s*(?:&nbsp;)?\s*\\[\\[(.+?)\\]\\]', r'{{player|$2|flag=$1}}', line)
	wikitext = mwparserfromhell.parse(new_line)
	for template in wikitext.filter_templates():
		if template.name.matches('player'):
			if template.has(2):
				display = template.get(2).value.strip()
				if display != '':
					link = template.get(1).value.strip()
					template.add(1, display)
					template.add('link', link)
					template.remove(2)
	return str(wikitext)

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
	lines = []
	for line in text.split('\n'):
		lines.append(fix_player(line))
	newtext = '\n'.join(lines)
	wikitext = mwparserfromhell.parse(text)
	for template in wikitext.filter_templates():
		if template.name.matches('player'):
			if template.has(1):
				val = template.get(1).value.strip()
				if '{{!}}' in val:
					names = val.split('{{!}}')
					template.add('link', names[0])
					template.add(1, names[1])
	newtext = str(wikitext)
	if text != newtext:
		print('Saving page %s...' % page.name)
		page.save(newtext, summary=summary)
	else:
		print('Skipping page %s...' % page.name)