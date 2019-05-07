from log_into_wiki import *
limit = -1
login('me')

with open('pages.txt', encoding="utf-8") as f:
	pages = f.readlines()
pages = [page.strip() for page in pages]

lmt = 0
for title in pages:
	if lmt == limit:
		break
	lmt += 1
	print('Deleting %s...' % title)
	site.api('delete',
			 title = title,
			 token = site.get_token('delete'),
			 reason = "Deleting files (equazcion's request)"
			 )