import urllib.request, time, sprite_creator, io, os
from log_into_wiki import *

SUFFIX = ''
SPRITE_NAME = 'SmiteRole'
IMAGE_DIR = 'Sprites/' + SPRITE_NAME + ' Images'
TEAM_DATA_FILE_LOCATION = SPRITE_NAME + 'Sprite' + SUFFIX + '.txt'
FILE_TYPE = 'png'
limit = -1
startat = None

site = login('me', 'smite-esports')
site_lol = login('me', 'lol')

if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

def get_country_name(file_name):
	return file_name.replace('.' + FILE_TYPE, '').replace('File:', '').replace('Square','')

pattern = r'.*src\=\"(.+?)\".*'
cat = site.categories['Role Icons']
for page in cat:
	to_parse_text = '[[%s|link=]]' % page.name
	result = site.api('parse', title = 'Main Page', text = to_parse_text, disablelimitreport = 1)
	parse_result_text = result['parse']['text']['*']
	url = re.match(pattern, parse_result_text)[1]
	image = urllib.request.urlopen(url).read()
	# image = Image.open(io.BytesIO(urllib.request.urlopen(url).read()))
	country = get_country_name(page.name)
	image_path = IMAGE_DIR + '/' + country + '.' + FILE_TYPE
	print(image_path)
	f = open(image_path, 'wb')
	f.write(image)
	f.close()
