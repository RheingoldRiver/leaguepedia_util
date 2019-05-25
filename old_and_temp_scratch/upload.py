from log_into_wiki import *
site = login('me', 'lol')

site.upload(open('RuneSprite.png', 'rb'), 'TeamSprite.png', 'Team Sprite', ignore=True)