from log_into_wiki import *
import mwparserfromhell

site = login('bot', 'lol')  # Set wiki
summary = 'Auto creating year player stats pages'  # Set summary

limit = -1
startat_page = 'Kedu'
print(startat_page)
# startat_page = 'asdf'
this_template = site.pages['Template:Infobox Player']  # Set template
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
	text = page.text()
	wikitext = mwparserfromhell.parse(text)
	res = site.api('cargoquery', tables="ScoreboardPlayer=SP,Tournaments",
				   join_on="SP.OverviewPage=Tournaments.OverviewPage",
				   fields="Tournaments.Year=Year",where='SP.Link="%s"' % page.name,group_by="Tournaments.Year")
	for item in res['cargoquery']:
		if 'Year' in item['title'] and item['title']['Year'] != '':
			year_page = page.name + '/Statistics/' + item['title']['Year']
			if site.pages[year_page].text() == '':
				print(site.pages[year_page].name)
				site.pages[year_page].save('{{PlayerTabsHeader}}\n{{PlayerYearStats}}',summary=summary)