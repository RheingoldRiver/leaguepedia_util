from log_into_wiki import *
import urllib.request
limit = -1

site = login('bot', 'lol')
tft = login('me', 'teamfighttactics')

with open('pages.txt', encoding="utf-8") as f:
	pages = f.readlines()

for page in pages:
	page = page.strip() + '.png'
	url = get_filename_url_to_open(site, page)
	img = urllib.request.urlopen(url).read()
	tft.upload(img, page, '[[Category:Item Images]]')