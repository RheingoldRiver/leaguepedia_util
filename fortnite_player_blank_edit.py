from river_mwclient.esports_client import EsportsClient
from river_mwclient.auth_credentials import AuthCredentials
from river_mwclient.extended_page import ExtendedPage

credentials = AuthCredentials(user_file="me")
site = EsportsClient('fortnite', credentials=credentials) #  set wiki

rc = site.recentchanges_by_interval(12 * 60, toponly=1)

data_pages = []

for p in rc:
	if p['title'].startswith('Data:'):
		data_pages.append(p['title'])

where = ' OR '.join(['TR._pageName="%s"' % _ for _ in data_pages])

players = site.cargo_client.page_list(
	tables="TournamentResults=TR,TournamentResults__RosterLinks=RL,_pageData=pd",
	join_on="TR._ID=RL._rowID, RL._value=pd._pageName",
	where='(%s) AND RL._rowID IS NOT NULL AND pd._pageName IS NOT NULL' % where,
	fields="RL._value=player"
)

for player in ExtendedPage.extend_pages(players):
	player.touch(check_existence=True)

# purge PR pages
for page in site.client.pages['Template:PRWiki'].embeddedin():
	page.purge()
