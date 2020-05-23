from river_mwclient.esports_client import EsportsClient
from river_mwclient.auth_credentials import AuthCredentials
from river_mwclient.template_modifier import TemplateModifierBase

credentials = AuthCredentials(user_file="bot")
site = EsportsClient('lol', credentials=credentials)  # Set wiki
summary = 'Use page_type instead of checkboxIsPersonality'  # Set summary


print(site.client.pages['Data:News/2020-05-17'])