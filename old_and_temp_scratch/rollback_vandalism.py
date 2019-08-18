import datetime
from log_into_wiki import *

site = login('me','spyro')

limit = -1

now = datetime.datetime.utcnow()
now_timestamp = now.isoformat()
then = now - datetime.timedelta(hours = 4) # change hours if needed
last_timestamp = then.isoformat()

revisions = site.api('query', format='json',
					 list='recentchanges',
					 rcstart=now_timestamp,
					 rcend=last_timestamp,
					 rcprop='title|ids',
					 rclimit='max',
					 rcdir = 'older'
					 )

pages = []
pages_used = {}
revs = {}
failed_pages = []

for revision in revisions['query']['recentchanges']:
	revs[revision['revid']] = True
	if revision['title'] in pages_used:
		pass
	else:
		pages.append(revision['title'])
		pages_used[revision['title']] = True

lmt = 0
for page in pages:
	if lmt == limit:
		break
	lmt += 1
	data = site.api('query',
		format = 'json',
		prop = 'revisions',
		titles = page,
		rvprop = 'content|ids',
		rvlimit = '50' # increase this if needed
	)
	datapages = data['query']['pages']
	text = ''
	print(page)
	thisrev = -1
	for pg in datapages: # loop of one thing
		print(pg)
		i = 0
		revlimit = len(datapages[pg]['revisions'])
		while i < revlimit:
			if datapages[pg]['revisions'][i]['revid'] in revs:
				pass
			else:
				thisrev = datapages[pg]['revisions'][i]['revid']
				text = datapages[pg]['revisions'][i]['*']
				break
			i += 1
	if thisrev == -1:
		failed_pages.append(page)
	else:
		p = site.pages[page]
		p.save(text,'Reverting oops')

if len(failed_pages) > 0:
	print('Printing list of pages that failed to revert. You may need to increase the rvlimit & rerun on them:')
	for p in failed_pages:
		print(p)
	
	with open('failed_pages.txt', 'w') as f:
		f.write('\n'.join(failed_pages))