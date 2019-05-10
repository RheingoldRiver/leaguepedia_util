import urllib.request, time, sprite_creator, io, os
from log_into_wiki import *

SUFFIX = ''
IMAGE_DIR = 'Flag Images'
DATA_FILE_LOCATION = 'flag_sprite_data' + SUFFIX + '.txt'
SPRITE_FILE_NAME = 'FlagSprite' + SUFFIX
IMAGE_WIDTH = 16
IMAGE_HEIGHT = 11
IMAGE_GAP = 2
IMAGES_ACROSS = 17
WLH_MIN_FOR_INCLUSION = 0

sprite = sprite_creator.Sprite(IMAGE_WIDTH, IMAGE_HEIGHT, IMAGES_ACROSS, IMAGE_GAP, SPRITE_FILE_NAME)
sprite.create_new()

print(sprite.sheet_width)

lines = []

for pos, fname in enumerate(os.listdir(IMAGE_DIR)):
	name = fname.replace('.png','')
	sprite.add_next_image_from_file(IMAGE_DIR + '/' + fname)
	lines.append('\t\t["{}"] = {{ pos = {}, section = 1 }},'.format(name, pos + 2))

with open(DATA_FILE_LOCATION, 'w') as f:
	f.write('\n'.join(lines))

sprite.save()