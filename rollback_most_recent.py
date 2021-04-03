from mwrogue.esports_client import EsportsClient
from mwcleric.auth_credentials import AuthCredentials
limit = -1

site = EsportsClient('lol', user_file="cod") # Set wiki

revisions = 2 # numver of revisions to roll back
comment = None # require the comment on the edit you're rolling back to be this
print(comment)
comment = "fixing toggle"

with open('pages.txt', encoding="utf-8") as f:
	pages = f.readlines()
pages = [page.strip() for page in pages]

lmt = 0
for page in pages:
	if lmt == limit:
		break
	lmt += 1
	data = site.client.api('query',
		format = 'json',
		prop = 'revisions',
		titles = page,
		rvprop = 'content|comment',
		rvlimit = revisions + 1
	)
	datapages = data['query']['pages']
	text = ''
	print(page)
	make_edit = comment
	for pg in datapages:
		# revisions is 1-indexed, but the api response is 0-indexed
		if comment:
			make_edit = datapages[pg]['revisions'][revisions-1]['comment'] == comment
		print(pg)
		text = datapages[pg]['revisions'][revisions]['*']
	if make_edit:
		p = site.client.pages[page]
		p.save(text,'Reverting oops')
	else:
		print("Skipping page %s because comment doesn't match" % page)
