from river_mwclient.esports_site import EsportsSite
import luacache_refresh, datetime

site = EsportsSite('lol', user_file="me") # Set wiki

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
	print(revision['title'])
	if revision['title'] == 'Module:Teamnames':
		luacache_refresh.teamnames(site)
		break
