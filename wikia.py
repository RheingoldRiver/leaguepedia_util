from log_into_wiki import *

site = log_into_fandom('me', 'leagueoflegends')

print(site.pages['Sona'].text())

