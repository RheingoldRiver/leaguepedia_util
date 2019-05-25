from log_into_wiki import *
import mwparserfromhell, sprite_creator
from team_sprite_entry import *
site = login('me','lol') # Set wiki
summary = 'Update team sprite according to high-use pages' # Set summary

SPRITE_NAME = 'Team'
IMAGE_WIDTH = 60
IMAGE_HEIGHT = 25
IMAGES_ACROSS = 15
IMAGE_GAP = 2
SPRITE_FILE_NAME = SPRITE_NAME + 'Sprite'
SPRITE_FILE_NAME_FULL = SPRITE_FILE_NAME + '.png'
SPRITE_DATA_PAGE = site.pages['Module:%sSprite' % SPRITE_NAME]
HIGH_USE_PAGE_LIST = site.pages['Maintenance:High-Use Pages'].text().split(',')

spritesheet = sprite_creator.Sprite(IMAGE_WIDTH, IMAGE_HEIGHT, IMAGES_ACROSS, IMAGE_GAP, SPRITE_FILE_NAME)
spritesheet.open_from_image(open_image_from_file(site, SPRITE_FILE_NAME_FULL))

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
	for team, pos in sprite_data.to_add.items():
		lmt += 1
		if lmt == limit:
			break
		print(team)
		try:
			img = open_image_from_file(site, team + 'logo std.png')
			spritesheet.add_image_at_location(img, pos)
		except Exception as e:
			continue

# for sprite in sprite_data.get_inactive_list():
# 	spritesheet.destroy(sprite.pos)
# 	sprite.destroy()

spritesheet.save()

new_sprite_text = sprite_file_table[0] + split_text + sprite_data.print_output() + end_text

if new_sprite_text != sprite_file_text:
	site.upload(open(SPRITE_FILE_NAME_FULL, "rb"), SPRITE_FILE_NAME_FULL, summary, ignore = True)
	SPRITE_DATA_PAGE.save(new_sprite_text, summary = summary)