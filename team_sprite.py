from river_mwclient.esports_client import EsportsClient
from river_mwclient.auth_credentials import AuthCredentials
import sprite_creator
from team_sprite_entry import *
from image_util import *
from mwclient.errors import APIError
credentials = AuthCredentials(user_file="me")
site = EsportsClient('lol', credentials=credentials) # Set wiki
summary = 'Update team sprite according to high-use pages' # Set summary

IMAGE_DIR = 'Test Images/'
SPRITE_NAME = 'Team'
IMAGE_WIDTH = 60
IMAGE_HEIGHT = 25
IMAGES_ACROSS = 15
IMAGE_GAP = 2
SPRITE_FILE_NAME = SPRITE_NAME + 'Sprite'
SPRITE_FILE_NAME_FULL = SPRITE_FILE_NAME + '.png'
SPRITE_DATA_PAGE = site.client.pages['Module:%sSprite' % SPRITE_NAME]
HIGH_USE_PAGE_LIST = site.client.pages['Maintenance:High-Use Pages'].text().split(',')

spritesheet = sprite_creator.Sprite(IMAGE_WIDTH, IMAGE_HEIGHT, IMAGES_ACROSS, IMAGE_GAP, SPRITE_FILE_NAME)
spritesheet.open_from_image(open_image_from_filename(site, SPRITE_FILE_NAME_FULL))

spritesheet.save()

split_text = '\tids = {\n'
end_text = '\n\t},\n}'

sprite_file_text = SPRITE_DATA_PAGE.text()
sprite_file_table = sprite_file_text.split(split_text)
sprite_text = sprite_file_table[1].replace(end_text, '').strip()
#print(sprite_file_table)
sprite_data = SpriteSheet(sprite_text)

limit = -1
lmt = 0
for title in HIGH_USE_PAGE_LIST:
	sprite_data.add_activity_from_wiki_page(site, title)
	for team, this_sprite in sprite_data.to_add.items():
		lmt += 1
		if lmt == limit:
			break
		print(team)
		try:
			url = get_filename_url_to_open(site, team + 'logo std.png')
			unversioned_url = re.sub(r'\?.*', '', url)
			if unversioned_url in sprite_data.urls_used:
				this_sprite.force_inactive()
			else:
				sprite_data.urls_used.append(unversioned_url)
				im = open_file_url(url)
				spritesheet.add_image_at_location(im, this_sprite.pos)
				this_sprite.set_file(unversioned_url)
		except Exception as e:
			this_sprite.force_inactive()
			print(e)
			print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
			continue

	for sprite in sprite_data.get_inactive_list():
		spritesheet.destroy(sprite.pos)
		sprite.destroy()

spritesheet.save()

new_sprite_text = sprite_file_table[0] + split_text + sprite_data.print_output() + end_text

if new_sprite_text != sprite_file_text:
	try:
		site.client.upload(open(SPRITE_FILE_NAME_FULL, "rb"), SPRITE_FILE_NAME_FULL, summary, ignore = True)
		SPRITE_DATA_PAGE.save(new_sprite_text, summary = summary)
		print('saved!')
	except APIError:
		print('no changes made')
