import urllib.request, time, sprite_creator, io, os
from river_mwclient.esports_client import EsportsClient
from river_mwclient.auth_credentials import AuthCredentials
import re

SUFFIX = '_min_30'
IMAGE_DIR = 'Team Images'
TEAM_DATA_FILE_LOCATION = 'spritedata' + SUFFIX + '.txt'
SPRITE_FILE_NAME = 'TeamSprite' + SUFFIX
IMAGE_WIDTH = 60
IMAGE_HEIGHT = 25
IMAGE_GAP = 2
IMAGES_ACROSS = 30
WLH_MIN_FOR_INCLUSION = 30
limit = -1
startat = None

credentials = AuthCredentials(user_file="me")
site = EsportsClient('lol', credentials=credentials) # Set wiki

teamnames_text = site.client.pages['Module:Teamnames'].text()
teamnames = []
for match in re.findall(r'link *= *\"(.+?)\"', teamnames_text):
	teamnames.append(match)
pattern = r'.*src\=\"(.+?)\".*'

sprite = sprite_creator.Sprite(IMAGE_WIDTH, IMAGE_HEIGHT, IMAGES_ACROSS, IMAGE_GAP, SPRITE_FILE_NAME)
sprite.create_new()

team_to_position_dict = {}
file_to_position_dict = {}

with open(TEAM_DATA_FILE_LOCATION, 'w+', encoding="utf-8") as f:
		f.write('')

def write_dict_entry(team):
	with open(TEAM_DATA_FILE_LOCATION, 'a+', encoding="utf-8") as f:
		f.write('\n' + team + '||' + str(team_to_position_dict[team]))

lmt = 0
for team in teamnames:
	lmt += 1
	if lmt == limit:
		break
	if startat and lmt < startat:
		continue
	result = site.client.api('query', list='backlinks', bltitle=team, bllimit=WLH_MIN_FOR_INCLUSION + 1)
	if len(result['query']['backlinks']) < WLH_MIN_FOR_INCLUSION + 1:
		print('%s has too few links, skipping' % team)
		continue
	# skip if the file is a redirect but record it as such for later
	file_page = 'File:%slogo std.png' % team
	file_text = site.client.pages[file_page].text().replace('_',' ')
	final_file_location = '%slogo std.png' % team.replace('.','')
	image_path = IMAGE_DIR + '/' + final_file_location
	if os.path.isfile(image_path):
		pass
	else:
		if 'redirect' in file_text.lower():
			final_file_location_match = re.match(r'.*File:(.*)\.png.*', file_text)
			if final_file_location_match:
				final_file_location = final_file_location_match[1].replace('.','') + '.png'
				if final_file_location in file_to_position_dict:
					team_to_position_dict[team] = file_to_position_dict[final_file_location]
					write_dict_entry(team)
					continue
			else:
				print('Failed to get file for %s' % team)
				continue
		final_file_location = final_file_location
		image_path = IMAGE_DIR + '/' + final_file_location
		if os.path.isfile(image_path):
			# save an api query if the image already exists locally
			pass
		else:
			# get the file from the wiki & download it
			to_parse_text = '[[%s|link=]]' % file_page
			result = site.client.api('parse', title = 'Main Page', text = to_parse_text, disablelimitreport = 1)
			parse_result_text = result['parse']['text']['*']
			url = re.match(pattern, parse_result_text)[1]
			image = urllib.request.urlopen(url).read()
			# image = Image.open(io.BytesIO(urllib.request.urlopen(url).read()))
			f = open(image_path, 'wb')
			f.write(image)
			f.close()
	try:
		sprite.add_next_image_from_file(image_path)
		team_to_position_dict[team] = sprite.current_location
		file_to_position_dict[final_file_location] = sprite.current_location
		write_dict_entry(team)
		print(str(sprite.current_location))
		sprite.save()
	except OSError:
		print('Failed to open %s' % image_path)

sprite.save()
print('Current location: %s' % str(sprite.current_location))
