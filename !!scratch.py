from user import User
from esports_site import EsportsSite

games = ['halo', 'smite', 'vg', 'rl', 'pubg', 'fortnite', 'apexlegends', 'fifa', 'gears', 'nba2k', 'paladins', 'siege',
         'default-loadout', 'commons', 'teamfighttactics']

site = EsportsSite('me', 'lol')

user = User(site, 'Ispoonz')

for game in games:
    if game != 'teamfighttactics':
        game = game + '-esports'
    new_site = EsportsSite('me', game)
    user.clone_rights(new_site)
