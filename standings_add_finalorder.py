from log_into_wiki import *
import mwparserfromhell

site = login('bot', 'lol')  # Set wiki
summary = 'Add finalorder in preparation for updating to new format'  # Set summary

limit = -1
startat_page = 'EU Challenger Series/2017 Season/Spring Qualifiers'
this_template = site.pages['Template:StandingsStart']  # Set template
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

standings_templates = [ 'StandingsLine/WL', 'StandingsLine/WLS', 'StandingsLine/WTLP', 'StandingsLine/WLP' ]

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
		standings_start = None
		multiple_standings = False
		one_standings = False
		teamlist = []
		for template in wikitext.filter_templates():
			if template.name.matches('StandingsStart'):
				standings_start = template
				teamlist = []
				if one_standings:
					multiple_standings = True
				one_standings = True
			elif [_ for _ in standings_templates if template.name.matches(_)]:
				if template.has('1'):
					teamlist.append(template.get('1').value.strip())
			elif template.name.matches('StandingsEnd'):
				if standings_start.has('places'):
					standings_start.add('finalorder', ','.join(teamlist), before = 'places')
				else:
					standings_start.add('finalorder', ','.join(teamlist))
			elif template.name.matches('TimelineOld') and not multiple_standings:
				template.add('finalorder', ','.join(teamlist))
		
		newtext = str(wikitext)
		if text != newtext:
			print('Saving page %s...' % page.name)
			page.save(newtext, summary=summary)
		else:
			print('Skipping page %s...' % page.name)