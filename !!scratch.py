import log_into_wiki

site = log_into_wiki.login('me', 'lol')

print(site.pages['Sami (Nicol\u00e1s Veliz)/Tournament Results'].text())
