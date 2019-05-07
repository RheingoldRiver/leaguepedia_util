from log_into_wiki import *
import mwparserfromhell

site = login('bot', 'terraria')  # Set wiki
summary = 'Separating recipes into its own template'  # Set summary

limit = -1
startat_page = 'Gray Brick Wall'
this_template = site.pages['Template:crafts row']  # Set template
pages = this_template.embeddedin()  # get the list of pages that transclude the template in question
# there are a lot of other ways to generate a list of pages, but this is probably the most standard that i use

pages_var = list(pages)  # in python you can only loop through

pages_array = [p.name for p in pages_var]

try:
	startat = pages_array.index(startat_page)
except NameError as e:
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
		for section in wikitext.get_sections(flat=True):
			is_recipe = False
			for heading in section.filter_headings():
				if heading.title.strip() == 'Recipe' or heading.title.strip() == 'Recipes':
					is_recipe = True
			if is_recipe:
				for template in section.filter_templates():
					if template.name.matches('crafts top'):
						template.name = 'recipes top'
					elif template.name.matches('crafts row'):
						template.name = 'recipes row'
					elif template.name.matches('crafts bottom'):
						template.name = 'recipes bottom'
		newtext = str(wikitext)
		if text != newtext:
			print('Saving page %s...' % page.name)
			page.save(newtext, summary=summary)
		else:
			print('Skipping page %s...' % page.name)