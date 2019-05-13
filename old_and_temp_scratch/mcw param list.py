from log_into_wiki import *
import mwparserfromhell

site = login('me','minecraft') # Set wiki
page = site.pages['Achievements']

this_template = 'Achievements'
this_param = 'title'

text = page.text()
wikitext = mwparserfromhell.parse(text)
arr = []
for template in wikitext.filter_templates():
	if template.name.matches(this_template):
		if template.has(this_param):
			arr.append(template.get(this_param).value.strip())
print(arr)