from log_into_wiki import *
import mwparserfromhell

site = login('bot', 'lol')  # Set wiki
summary = 'GS4 -> GS5'  # Set summary

limit = -1
# startat_page = 'asdf'
this_template = site.pages['Template:GameSchedule5']  # Set template
pages = this_template.embeddedin()

pages_var = list(pages)

pages_array = [p.name for p in pages_var]

add_to_start = [ 'hide', 'title', 'norounds', 'customwidth', 'dst' ]

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
			if template.name.matches('GameSchedule5'):
				
				if template.has('start'):
					start = template.get('start').value.strip()
					if start != '':
						tl2 = mwparserfromhell.nodes.template.Template(name="GameSchedule5/Start")
						if template.has('hide'):
							tl2.add('hide', template.get('hide').value.strip())
						template.name = 'replacethis'
				if template.has('end'):
					end_val = template.get('end').value.strip()
					if end_val != '':
						tl2 = mwparserfromhell.nodes.template.Template(name="GameSchedule5/End")
						
						
				
		
		newtext = str(wikitext)
		if text != newtext:
			print('Saving page %s...' % page.name)
			page.save(newtext, summary=summary)
		else:
			print('Skipping page %s...' % page.name)