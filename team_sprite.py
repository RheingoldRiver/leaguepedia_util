from log_into_wiki import *
import mwparserfromhell, sprite_creator

site = login('me','lol') # Set wiki
summary = 'Update team sprite according to high-use pages' # Set summary

SPRITE_NAME = 'Champion'
IMAGE_WIDTH = 60
IMAGE_HEIGHT = 25
IMAGES_ACROSS = 15
IMAGE_GAP = 2
SPRITE_FILE_NAME = SPRITE_NAME + 'Sprite'

team_sprite = sprite_creator.Sprite(IMAGE_WIDTH, IMAGE_HEIGHT, IMAGES_ACROSS, IMAGE_GAP, SPRITE_FILE_NAME)
team_sprite.open_from_url(site)


