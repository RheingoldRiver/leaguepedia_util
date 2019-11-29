from log_into_wiki import *
import mwparserfromhell

site = login('me', 'lol')  # Set wiki


for page in site.allpages(namespace=10018):
    print(page.name)
    site.api('review', revid=page.revision, token = site.get_token('csrf'))
