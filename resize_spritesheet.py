import urllib.request, time, sprite_creator, io, os
from log_into_wiki import *

SUFFIX = ''
SPRITE_NAME = 'Item'
IMAGE_DIR = SPRITE_NAME + ' Images'
DATA_FILE_LOCATION = SPRITE_NAME + 'Sprite' + SUFFIX + '.txt'
IMAGE_WIDTH = 30
IMAGE_HEIGHT = 30
IMAGE_GAP = 2
IMAGES_ACROSS = 20

OLD_FILE = 'ItemSprite Old'
SPRITE_FILE_NAME = SPRITE_NAME + 'Sprite' + SUFFIX

sprite = sprite_creator.Sprite(IMAGE_WIDTH, IMAGE_HEIGHT, IMAGES_ACROSS, IMAGE_GAP, SPRITE_FILE_NAME)
sprite.create_new()

sprite_old = sprite_creator.Sprite(64, 64, 20, 2, OLD_FILE)
sprite_old.open_from_file(OLD_FILE)

for i in range(1, 500):
	img = sprite_old.get_slice(i)
	sprite.add_next_image(img)
	print(sprite.current_location)
	print('{} {}'.format(sprite_old.current_row, sprite_old.current_col))
	
sprite.save()