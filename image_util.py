from PIL import Image, ImageFile
from mwcleric.wiki_client import WikiClient

ImageFile.LOAD_TRUNCATED_IMAGES = True
import re, urllib.request, io

def get_filename_url_to_open(site: WikiClient, filename, size=None):
	pattern = r'.*src\=\"(.+?)\".*'
	size = '|' + str(size) + 'px' if size else ''
	filename = filename.replace('File:', '')
	to_parse_text = '[[File:{}|link=%s]]'.format(filename, size)
	result = site.client.api('parse', title='Main Page', text=to_parse_text, disablelimitreport=1)
	parse_result_text = result['parse']['text']['*']
	url = re.match(pattern, parse_result_text)[1]
	return url

def open_file_url(url):
	final_url = url + '&format=original'
	return Image.open(io.BytesIO(urllib.request.urlopen(final_url).read()))

def open_image_from_filename(site: WikiClient, filename, size=None):
	url = get_filename_url_to_open(site, filename, size=size)
	return open_file_url(url)
