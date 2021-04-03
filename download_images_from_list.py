from mwrogue.esports_client import EsportsClient
from mwcleric.auth_credentials import AuthCredentials
import os
from image_util import *

limit = -1

credentials = AuthCredentials(user_file="me")
site = EsportsClient('lol', credentials=credentials) # Set wiki

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
