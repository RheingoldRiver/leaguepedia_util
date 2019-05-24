from log_into_wiki import *
import mwparserfromhell

site = login('bot','lol') # Set wiki
summary = 'Bot Edit' # Set summary

limit = -1
startat_page = None
print(startat_page)
#startat_page = 'asdf'
for year in ["2015", "2016", "2017", "2018", "2019"]:
	this_template = site.pages['Template:ChampStatsPage/' + year] # Set template
	pages = this_template.embeddedin()
	
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
		print('Saving page %s' % page.name)
		page.save('{{ChampionYearStatsPage}}')