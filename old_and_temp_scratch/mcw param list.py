from river_mwclient.esports_site import EsportsSite
import mwparserfromhell

site = EsportsSite('lol')'minecraft') # Set wiki
page = site.client.pages['Achievements']

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
