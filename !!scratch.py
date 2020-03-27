from river_mwclient.esports_client import EsportsClient
from river_mwclient.auth_credentials import AuthCredentials
from river_mwclient.template_modifier import TemplateModifierBase
from river_mwclient.page_modifier import PageModifierBase

credentials = AuthCredentials(user_file="bot")
site = EsportsClient('lol', credentials=credentials)  # Set wiki
summary = 'Move skin page names'  # Set summary

files = site.cargo_client.query(fields="_pageName=Page, Name, ImageType", tables="SkinImages", limit="max")

for file in files:
    print(file['Page'])
    if 'File:Skin ' in file['Page']:
        continue
    if file['ImageType'] == 'Square':
        continue
    file_type = file['Page'].split('.')[1]
    new_name = 'File:Skin {} {}.{}'.format(file['ImageType'], file['Name'], file_type)
    print(new_name)
    skin_page = site.client.pages[file['Page']]
    if 'redirect' in skin_page.text().lower():
        continue
    skin_page.move(new_name)
