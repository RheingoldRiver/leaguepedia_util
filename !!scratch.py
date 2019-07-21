from log_into_wiki import *
import weekly_utils as utils

site = login('me', 'lol')  # Set wiki


utils.make_doc_pages(site, site.pages['Module:Bracket/2SE'])
