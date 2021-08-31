from mwcleric.auth_credentials import AuthCredentials
from mwrogue.esports_client import EsportsClient

limit = -1
# startat_page = 'Gamelord'
template = 'Infobox Player'
form = 'Infobox Player'

credentials = AuthCredentials(user_file="bot")
site = EsportsClient('lol', credentials=credentials)  # Set wiki

########################################

result = site.pages_using(template, generator=False)

pages = []

for p in result:
	pages.append(p)

try:
	startat = pages.index(startat_page)
except NameError as e:
	startat = -1
except ValueError as e:
	startat = -1
failures = []

lmt = 0
for page in pages:
	if lmt == limit:
		break
	lmt += 1
	print(page)
	if lmt <= startat:
		pass
	else:
		try:
			site.client.api('pfautoedit', format='json',
			                form=form,
			                target=page
			                )
		except Exception as e:
			failures.append(page + "(" + e.args[0] + ")")

print('Done! Printing failures...')

for failure in failures:
	print(failure)
