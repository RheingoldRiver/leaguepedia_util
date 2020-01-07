from log_into_wiki import *

site = login('me', 'commons')  # Set wiki
for file in site.categories['Media Icons']:
	redirect = site.pages[file.name.replace('.png', 'logo std.png')]
	if redirect.exists:
		redirect.delete()
