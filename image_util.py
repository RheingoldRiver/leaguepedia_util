from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
import re, urllib.request, io

def get_filename_url_to_open(site, filename, size=None):
	pattern = r'.*src\=\"(.+?)\".*'
	size = '|' + str(size) + 'px' if size else ''
	to_parse_text = '[[File:{}|link=%s]]'.format(filename, size)
	result = site.client.api('parse', title='Main Page', text=to_parse_text, disablelimitreport=1)
	parse_result_text = result['parse']['text']['*']
	print(parse_result_text)
	url = re.match(pattern, parse_result_text)[1]
	return url

def open_file_url(url):
	return Image.open(io.BytesIO(urllib.request.urlopen(url).read()))

def open_image_from_filename(site, filename, size=None):
	url = get_filename_url_to_open(site, filename, size=size)
	return open_file_url(url)
