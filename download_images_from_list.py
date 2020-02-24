from river_mwclient.esports_site import EsportsSite
import os
import re, urllib.request, io
from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

limit = -1

site = EsportsSite('lol', user_file="me") # Set wiki

LOC = 'Sprites/' + 'League Images'

with open('pages.txt', encoding="utf-8") as f:
	pages = f.readlines()

# These files were originally in log_into_wiki but since we are ditching that, they are copied here
# Probably some ImageUtil or something should be made
# Maybe some of these would even make sense to add to ExtendedSite

def get_filename_url_to_open(site, filename, size=None):
	pattern = r'.*src\=\"(.+?)\".*'
	size = '|' + str(size) + 'px' if size else ''
	to_parse_text = '[[File:{}|link=%s]]'.format(filename, size)
	result = site.api('parse', title='Main Page', text=to_parse_text, disablelimitreport=1)
	parse_result_text = result['parse']['text']['*']
	print(parse_result_text)
	url = re.match(pattern, parse_result_text)[1]
	return url

def open_file_url(url):
	return Image.open(io.BytesIO(urllib.request.urlopen(url).read()))

def open_image_from_filename(site, filename, size=None):
	url = get_filename_url_to_open(site, filename, size=size)
	return open_file_url(url)

for page in pages:
	page = page.strip()
	if os.path.isfile(LOC + '/' + page) or os.path.isfile(LOC + '/' + page.replace(' ','_')):
		pass
	else:
		img = open_image_from_filename(site, page)
		img.save(LOC + '/' + page, 'png')
