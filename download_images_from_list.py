from log_into_wiki import *
import os
limit = -1

site = login('bot', 'lol')

LOC = 'Sprites/' + 'League Images'

with open('pages.txt', encoding="utf-8") as f:
	pages = f.readlines()

for page in pages:
	page = page.strip()
	if os.path.isfile(LOC + '/' + page) or os.path.isfile(LOC + '/' + page.replace(' ','_')):
		pass
	else:
		img = open_image_from_filename(site, page)
		img.save(LOC + '/' + page, 'png')