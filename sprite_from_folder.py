import urllib.request, time, sprite_creator, io, os
from log_into_wiki import *

SUFFIX = ''
SPRITE_NAME = 'League'
IMAGE_DIR = SPRITE_NAME + ' Images'
DATA_FILE_LOCATION = SPRITE_NAME + 'Sprite' + SUFFIX + '.txt'
IMAGE_WIDTH = 25
IMAGE_HEIGHT = 25
IMAGE_GAP = 2
IMAGES_ACROSS = 17

SPRITE_FILE_NAME = SPRITE_NAME + 'Sprite' + SUFFIX

sprite = sprite_creator.Sprite(IMAGE_WIDTH, IMAGE_HEIGHT, IMAGES_ACROSS, IMAGE_GAP, SPRITE_FILE_NAME)
sprite.create_new()

lines = [
"""return {{
	settings = {{
		align = 'middle',
		autolinksuffix = '',
		defaultlengthkey = 'link',
		defaultlinkkey = 'link',
		height = {},
		lookup = 'SPRITENAMEnames',
		name = 'SPRITENAME',
		nourl = 'Yes',
		sheetsize = {},
		spacing = {},
		stylesheet = true,
		url = require( [[Module:Sprite]] ).getUrl( 'SPRITENAMESprite.png'),
		width = {},
	}},
	sections = {{
		{{ name = 'Uncategorized', id = 1 }},
	}},
	ids = {{""".format(str(IMAGE_HEIGHT), str(sprite.sheet_width), str(IMAGE_GAP), str(IMAGE_WIDTH)).replace('SPRITENAME', SPRITE_NAME)
 ]

for pos, fname in enumerate(os.listdir(IMAGE_DIR)):
	name = fname.replace('.png','')
	sprite.add_next_image_from_file(IMAGE_DIR + '/' + fname)
	lines.append('\t\t["{}"] = {{ pos = {}, section = 1 }},'.format(name, pos + 2))

lines.append('\t\t["{}"] = {{ pos = {}, section = 1 }},'.format('unknown', '1'))

lines.append('	},')
lines.append('}')

with open(DATA_FILE_LOCATION, 'w', encoding="utf-8") as f:
	f.write('\n'.join(lines))

sprite.save()