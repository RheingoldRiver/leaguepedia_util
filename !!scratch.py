from user import User
from esports_site import EsportsSite

site = EsportsSite('me', 'lol')

user = User(site, 'Ispoonz')

for new_site in site.other_sites():
    user.clone_rights(new_site)
