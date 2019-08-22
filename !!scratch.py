from log_into_wiki import *
import mwparserfromhell

site = login('bot', 'lol')  # Set wiki


p = site.pages['League of Legends Wiki']
t = p.text()
print (p.edit_time)
