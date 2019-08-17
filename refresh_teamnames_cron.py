from log_into_wiki import *
import luacache_refresh, datetime

site = login('me', 'lol')

now = datetime.datetime.utcnow()
then = now - datetime.timedelta(minutes=1)

revisions = site.api('query',
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
