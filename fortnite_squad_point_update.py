from log_into_wiki import *
import mwparserfromhell
from mwclient.page import Page

PLAYERS_PER_SQUAD = 4
CURRENT_YEAR = 2020
CURRENT_YEAR_STR = str(CURRENT_YEAR)

site = login('me', 'fortnite-esports')  # Set wiki
summary = 'Automatic Squad Update'  # Set summary

def run():
	pages = get_pages()
	for page in pages:
		lookup = get_player_squads(page)
		update_and_save(page, lookup)

def get_pages():
	this_template = site.pages['Template:Listplayer/Current']  # Set template
	return this_template.embeddedin(namespace=0)

def get_player_squads(page:Page):
	# we will assume that LPC name exactly matches player page name
	# otherwise we need an extra copy of PR and ew
	table_list = [
		"ListplayerCurrent=LPC",
		"PlayerRedirects=PR",
		"TournamentResults__RosterLinks=RL",
		"TournamentResults=Res",
		"Tournaments=T"
	]
	join_list = [
		"LPC.Link=PR._pageName",
		"PR.AllName=RL._value",
		"RL._rowID=Res._ID",
		"Res.OverviewPage=T._pageName",
	]
	where = [
		'LPC._pageName="%s"' % page.name,
		'(T.Date >= "{}-01-01" AND T.Date <= "{}-12-31")'.format(
			CURRENT_YEAR_STR, CURRENT_YEAR_STR
		)
	]
	# print(','.join(table_list))
	# print(','.join(join_list))
	# print(' AND '.join(['(%s)' % _ for _ in where]))
	result = site.cargoquery(
		tables=','.join(table_list),
		join_on = ','.join(join_list),
		group_by = 'PR._pageName',
		fields = 'LPC.Link=Link, SUM(Res.PRPoints)=Points',
		where = ' AND '.join(['(%s)' % _ for _ in where]),
		order_by = 'SUM(Res.PRPoints) DESC'
	)
	lookup_table = {}
	# we can assume this is sorted bc of the order_by
	squad = 1
	counter = 0
	for line in result:
		if counter == PLAYERS_PER_SQUAD:
			squad +=1
			counter = 0
		lookup_table[line['Link']] = squad
		counter += 1
	return lookup_table

def update_and_save(page, lookup):
	text = page.text()
	wikitext = mwparserfromhell.parse(text)
	for template in wikitext.filter_templates():
		if tl_matches(template, ['Listplayer/Current']):
			player = template.get('1').value.strip()
			if player not in lookup:
				template.add('squad', '')
				continue
			template.add('squad', lookup[player])
	
	newtext = str(wikitext)
	if text != newtext:
		print('Saving page %s...' % page.name)
		page.save(newtext, summary=summary)
	else:
		print('Skipping page %s...' % page.name)

if __name__ == '__main__':
	run()
