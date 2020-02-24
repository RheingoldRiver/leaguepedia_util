from river_mwclient.esports_site import EsportsSite
site = EsportsSite('lol', user_file='me')

site.upload(open('RuneSprite.png', 'rb'), 'TeamSprite.png', 'Team Sprite', ignore=True)
