from river_mwclient.esports_client import EsportsClient
from river_mwclient.auth_credentials import AuthCredentials
from mwparserfromhell import parse
from mwclient.page import Page

TOOLTIP_TEXT = '{{PlayerTooltip}}'

credentials = AuthCredentials(user_file="bot")
site = EsportsClient('lol', credentials=credentials)  # Set wiki
summary = 'Bot edit'  # Set summary

for page in site.client.categories['Players']:
	page: Page
	tooltip_page = 'Tooltip:{}'.format(page.name)
	print(tooltip_page)
	site.client.pages[tooltip_page].save(TOOLTIP_TEXT)