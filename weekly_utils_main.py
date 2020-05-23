# weekly is a lie, this runs twice-daily

import datetime
import scrape_runes
from river_mwclient.esports_client import EsportsClient
from river_mwclient.auth_credentials import AuthCredentials

credentials = AuthCredentials(user_file="me")
site = EsportsClient('lol', credentials=credentials) # Set wiki

now_timestamp = datetime.datetime.utcnow().isoformat()
with open('daily_last_run.txt','r') as f:
	last_timestamp = f.read()
with open('daily_last_run.txt','w') as f:
	f.write(now_timestamp)

revisions = site.client.api('query', format='json',
					 list='recentchanges',
					 rcstart=now_timestamp,
					 rcend=last_timestamp,
					 rcprop='title|ids|patrolled',
					 rclimit='max',
					 rctoponly=1, # commented bc we need all revisions to patrol user pages
					 rcdir = 'older'
					 )

pages = []
pages_for_runes = []

for revision in revisions['query']['recentchanges']:
	title = revision['title']
	if title not in pages:
		pages.append(title)
		if title.startswith('Data:'):
			pages_for_runes.append(title)

success_page = site.client.pages['User:RheingoldRiver/Maint Log']
text = success_page.text()
text = text + '\nScript finished maint successfully: ' + now_timestamp
try:
	scrape_runes.scrape(site, pages_for_runes, False)
	text = text + '\nScript finished regular runes successfully: ' + now_timestamp
except Exception as e:
	text = text + '\nException running regular runes: ' + str(e) + ' ' + now_timestamp
try:
	scrape_runes.scrapeLPL(site, pages_for_runes, False)
	text = text + '\nScript finished everything successfully: ' + now_timestamp
except Exception as e:
	text = text + '\nException running LPL runes: ' + str(e) + ' ' + now_timestamp
success_page.save(text,tags='daily_errorfix')
