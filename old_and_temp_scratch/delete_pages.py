from log_into_wiki import *
limit = -1
site = login('bot', 'lol')

pages = site.allpages(namespace=108)

lmt = 0
for page in pages:
	if lmt == limit:
		break
	lmt += 1
	site.api('delete',
			 title = page.name,
			 token = site.get_token('delete'),
			 reason = "oops i forgot to change the summary lol bye concepts"
			 )