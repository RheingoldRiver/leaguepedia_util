from user import User
from esports_site import EsportsSite

site = EsportsSite('me', 'halo')

for new_site in site.other_sites():
    user = User(new_site, 'Ispoonz')
    print(user.groups)
    user.add_rights(['sysop'])
    print(user.groups)
