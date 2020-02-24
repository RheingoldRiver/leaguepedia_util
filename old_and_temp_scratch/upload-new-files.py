import os

from river_mwclient.esports_site import EsportsSite

site = EsportsSite('lol') 'thealchemistcode')

path = 'S:/Documents/Wikis/Python/files for thealchemistcode'

for f in os.listdir(path):
	page = site.client.pages[f.replace('_','/').replace('.txt','').replace('COLON',':')]
	with open(path + '/' + f, encoding='utf-8') as thisfile:
		text = thisfile.read()
	page.save(text,'attempting to import data')
