import urllib.request, time, sprite_creator, io, os
from log_into_wiki import *

SUFFIX = ''
SPRITE_NAME = 'Champion'
IMAGE_DIR = SPRITE_NAME + ' Images'
TEAM_DATA_FILE_LOCATION = SPRITE_NAME + 'Sprite' + SUFFIX + '.txt'
limit = -1
startat = None

site = login('me', 'commons-esports')
site_lol = login('me', 'lol')

def get_country_name(file_name):
	return file_name.replace('Square', '').replace('.png', '').replace('File:', '')

pattern = r'.*src\=\"(.+?)\".*'
cat = site_lol.categories['Champions']
for page in cat:
	to_parse_text = '[[File:%sSquare.png|link=]]' % page.name
	result = site_lol.api('parse', title = 'Main Page', text = to_parse_text, disablelimitreport = 1)
	parse_result_text = result['parse']['text']['*']
	url = re.match(pattern, parse_result_text)[1]
	image = urllib.request.urlopen(url).read()
	# image = Image.open(io.BytesIO(urllib.request.urlopen(url).read()))
	country = get_country_name(page.name)
	image_path = IMAGE_DIR + '/' + country + '.png'
	print(image_path)
	f = open(image_path, 'wb')
	f.write(image)
	f.close()