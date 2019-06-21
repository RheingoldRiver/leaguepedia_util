from log_into_wiki import *
import weekly_utils as utils
import mwparserfromhell

site = login('me', 'lol')  # Set wiki
summary = 'remove all extra mhp params/text'  # Set summary

page = site.pages['Data:2012 MLG Pro Circuit/Fall/Championship']

wikitext = mwparserfromhell.parse(page.text())

utils.set_initial_order(wikitext)

page.save(str(wikitext))