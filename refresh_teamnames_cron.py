from river_mwclient.esports_client import EsportsClient
from river_mwclient.auth_credentials import AuthCredentials
import luacache_refresh, datetime

credentials = AuthCredentials(user_file="me")
site = EsportsClient('lol', credentials=credentials) # Set wiki

now = datetime.datetime.utcnow()
then = now - datetime.timedelta(minutes=1)

revisions = site.client.api('query',
					 list="recentchanges",
					 rcstart = now.isoformat(),
					 rcend = then.isoformat(),
					 rcprop = 'title',
					 rclimit = 'max',
					 rctoponly = '1',
					 rcdir = 'older'
					 )

for revision in revisions['query']['recentchanges']:
	# print(revision['title'])
	if revision['title'] == 'Module:Teamnames':
		luacache_refresh.teamnames(site)
		break
