from river_mwclient.esports_site import EsportsSite
import os
from image_util import *

limit = -1

site = EsportsSite('lol', user_file="me") # Set wiki

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
