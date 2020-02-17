from log_into_wiki import *
import mwparserfromhell

site = login('bot', 'lol')  # Set wiki

template_name = 'PicksAndBansS7'
orig_params = ['team1', 'team2']
new_params = ['blueteam', 'redteam']

param_summary = []
for i, orig in enumerate(orig_params):
	param_summary.append('{} -> {}'.format(orig, new_params[i]))
summary = 'Param replacement: {}'.format(';'.join(param_summary)) # Set summary

limit = -1
startat_page = 'ESL A1 Adria/Season 2 Playoffs/Picks and Bans/Offline Playoffs'
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

exceptions = []

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
				for i, orig_param in enumerate(orig_params):
					if template.has(orig_param):
						template.get(orig_param).name = new_params[i]
		
		newtext = str(wikitext)
		if text != newtext:
			try:
				print('Saving page %s...' % page.name)
				page.save(newtext, summary=summary)
			except Exception as e:
				exceptions.append(page.name)
		else:
			print('Skipping page %s...' % page.name)
print('Exceptions:')
print('\n'.join(exceptions))
