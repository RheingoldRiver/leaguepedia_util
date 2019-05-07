import scrape_runes
from log_into_wiki import *

site = login('me','lol') # Set wiki

pages = ['Data:LPL/2019 Season/Spring Season', 'Data:LPL/2019 Season/Spring Season/2']

#pages = ['Data:OPL/2019 Season/Split 1/2']

#scrape_runes.scrape(site, pages, False)
scrape_runes.scrapeLPL(site, pages, False)