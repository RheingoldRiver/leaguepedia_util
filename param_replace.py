from log_into_wiki import *
import mwparserfromhell

site = login('bot', 'teamfighttactics')  # Set wiki

template_name = 'Infobox Item'
orig_param = 'concept'
new_param = 'tournament'

summary = 'Param replacement: {0} -> {1}'.format(orig_param, new_param) # Set summary

limit = -1
# startat_page = 'asdf'
this_template = site.pages['Template:' + template_name]  # Set template
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
	else:
		text = page.text()
		wikitext = mwparserfromhell.parse(text)
		for template in wikitext.filter_templates():
			if template.name.matches(template_name):
				if template.has(orig_param):
					template.get(orig_param).name = new_param
		
		newtext = str(wikitext)
		if text != newtext:
			print('Saving page %s...' % page.name)
			page.save(newtext, summary=summary)
		else:
			print('Skipping page %s...' % page.name)
