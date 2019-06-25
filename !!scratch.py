from log_into_wiki import *
import mwparserfromhell

site = login('me', 'fortnite-esports')  # Set wiki
summary = 'Bot Edit'  # Set summary

for page in site.allpages():
	if page.text() == '':
		print(page.name)
