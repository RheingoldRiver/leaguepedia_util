import os

from log_into_wiki import *

site = login('me', 'thealchemistcode')

path = 'S:/Documents/Wikis/Python/files for thealchemistcode'

for f in os.listdir(path):
	page = site.pages[f.replace('_','/').replace('.txt','').replace('COLON',':')]
	with open(path + '/' + f, encoding='utf-8') as thisfile:
		text = thisfile.read()
	page.save(text,'attempting to import data')