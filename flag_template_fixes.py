from log_into_wiki import *
import mwparserfromhell

site = login('me','lol') # Set wiki
summary = 'Fix more language flags' # Set summary

limit = -1
startat_page = 'ESL Euro Series/Summer 2014'
this_template = site.pages['Template:Stream'] # Set template
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

def fix_line_flags(line):
	wikiline = mwparserfromhell.parse(line)
	templates_to_remove = []
	flags_to_add = []
	has_stream = False
	for template in wikiline.filter_templates():
		if template.name.matches('flag'):
			templates_to_remove.append(template)
			if template.has(1):
				flags_to_add.append(str(template.get(1).value.strip()))
		if template.name.matches('stream'):
			has_stream = True
			if flags_to_add:
				if template.has('lang'):
					old_flags = template.get('lang').value.strip()
					new_flags = ','.join(flags_to_add)
					lang_new = old_flags + ',' + new_flags
					template.add('lang', lang_new)
	if has_stream:
		for template in templates_to_remove:
			wikiline.remove(template)
	return str(wikiline)

lmt = 0
for page in pages_var:
	if lmt == limit:
		break
	lmt += 1
	if lmt < startat:
		print("Skipping page %s" % page.name)
		continue
	print(page.name)
	text = page.text()
	lines = []
	for line in text.split('\n'):
		lines.append(fix_line_flags(line))
	newtext = '\n'.join(lines)
	if text != newtext:
		print('Saving page %s...' % page.name)
		page.save(newtext, summary=summary)
	else:
		print('Skipping page %s...' % page.name)