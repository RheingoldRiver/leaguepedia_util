from river_mwclient.esports_site import EsportsSite
import mwparserfromhell, re

site = EsportsSite('fortnite', user_file="me") # Set wiki
summary = 'Changing links/display to be just 1 field, with link only'  # Set summary

limit = -1
startat_page = None
print(startat_page)
#startat_page = 'Data:LCK/2018 Season/Summer Playoffs'
this_template = site.client.pages['Template:Infobox Tournament']  # Set template
pages = this_template.embeddedin()

# with open('pages.txt', encoding="utf-8") as f:
# 	pages = f.readlines()

#pages = [site.pages['Data:Challengers Korea/2019 Season/Spring Season']]

params = ['player','player1']

def links_to_display(template, param):
	if not template.has(param):
		return
	if (not template.has(param + 'link')) and (not template.has(param + 'links')):
		return
	suffix = 'link'
	if not template.has(param + suffix):
		suffix = 'links'
	display_str = template.get(param).value.strip()
	link_str = template.get(param + suffix).value.strip()
	displays = display_str.split(',')
	links = link_str.split(',')
	new = []
	for i, v in enumerate(displays):
		if i < len(links) and links[i] != '':
			uc_display = v[0].upper() + v[1:]
			regex = r'^' + re.escape(uc_display)
			link = re.sub(regex, v, links[i])
			new.append(link)
			continue
		new.append(v)
	template.add(param, ','.join(new))
	template.remove(param + suffix)

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
	wikitext = mwparserfromhell.parse(text)
	for template in wikitext.filter_templates():
		if template.name.matches(['TournamentResultsLineDuos', 'TournamentResultsLineSolo']):
			for param in params:
				links_to_display(template, param)
	
	newtext = str(wikitext)
	if text != newtext:
		print('Saving page %s...' % page.name)
		page.save(newtext, summary=summary)
	else:
		print('Skipping page %s...' % page.name)
