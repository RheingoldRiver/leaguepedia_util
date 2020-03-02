import urllib.request, time, sprite_creator, io, os
from river_mwclient.esports_client import EsportsClient
from river_mwclient.auth_credentials import AuthCredentials
import re

SUFFIX = ''
SPRITE_NAME = 'Champion'
IMAGE_DIR = SPRITE_NAME + ' Images'
TEAM_DATA_FILE_LOCATION = SPRITE_NAME + 'Sprite' + SUFFIX + '.txt'
limit = -1
startat = None

credentials = AuthCredentials(user_file="me")
site = EsportsClient('commons', credentials=credentials) #  set wiki
site_lol = EsportsClient('lol', credentials=credentials) #  set wiki

def get_country_name(file_name):
	return file_name.replace('Square', '').replace('.png', '').replace('File:', '')

pattern = r'.*src\=\"(.+?)\".*'
cat = site_lol.client.categories['Champions']
for page in cat:
	to_parse_text = '[[File:%sSquare.png|link=]]' % page.name
	result = site_lol.client.api('parse', title = 'Main Page', text = to_parse_text, disablelimitreport = 1)
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
