import urllib.request, time, sprite_creator, io, os
from log_into_wiki import *

SUFFIX = ''
IMAGE_DIR = 'Flag Images'
TEAM_DATA_FILE_LOCATION = 'flag_sprite_data' + SUFFIX + '.txt'
SPRITE_FILE_NAME = 'FlagSprite' + SUFFIX
IMAGE_WIDTH = 16
IMAGE_HEIGHT = 11
IMAGE_GAP = 2
IMAGES_ACROSS = 17
WLH_MIN_FOR_INCLUSION = 0
limit = -1
startat = None

site = login('me', 'commons-esports')
site_lol = login('me', 'lol')

def get_country_name(file_name):
	abb = file_name.replace('File:', '').replace('.png', '')
	result = site_lol.api('parse', title = 'Main Page', text = '!!!!{{Country|' + abb + '}}!!!!', disablelimitreport = 1)
	result_text = result['parse']['text']['*']
	country_name = re.search(r'!!!!(.*)!!!!', result_text)[1]
	print(country_name)
	return country_name

pattern = r'.*src\=\"(.+?)\".*'
cat = site.categories['Flags']
for page in cat:
	to_parse_text = '[[%s|link=]]' % page.name
	result = site.api('parse', title = 'Main Page', text = to_parse_text, disablelimitreport = 1)
	parse_result_text = result['parse']['text']['*']
	url = re.match(pattern, parse_result_text)[1]
	image = urllib.request.urlopen(url).read()
	# image = Image.open(io.BytesIO(urllib.request.urlopen(url).read()))
	country = get_country_name(page.name)
	image_path = IMAGE_DIR + '/' + country + '.png'
	f = open(image_path, 'wb')
	f.write(image)
	f.close()