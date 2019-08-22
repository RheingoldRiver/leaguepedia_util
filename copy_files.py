from log_into_wiki import *
import urllib.request

site = login('me', 'spyro')  # Set wiki
tft = login('me', 'wikisandbox')
summary = 'Copying image?'  # Set summary


limit = -1

for page in site.allpages(namespace=6):
	url = get_filename_url_to_open(site, page.name.replace('File:',''))
	try:
		img = urllib.request.urlopen(url).read()
		tft.upload(img, page.name, '[[Category:Images copied from Spyro]]')
	except Exception as e:
		print(e)
