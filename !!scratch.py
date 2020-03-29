import re
from river_mwclient.esports_client import EsportsClient
from river_mwclient.auth_credentials import AuthCredentials
from river_mwclient.template_modifier import TemplateModifierBase
from river_mwclient.page_modifier import PageModifierBase
from mwparserfromhell import parse
from mwparserfromhell.nodes.template import Template

credentials = AuthCredentials(user_file="bot")
site = EsportsClient('lol', credentials=credentials)  # Set wiki
summary = 'Split gallery pages into multiple tabs'  # Set summary

for champion_page in site.client.categories['Champions']:
    champion = champion_page.name
    if champion_page.name < 'Senna':
        continue
    print(champion)
    gallery_page = site.client.pages[champion + '/Gallery/Loading Screens']
    text = gallery_page.text()
    wikitext = parse(text)
    for template in wikitext.filter_templates():
        template: Template
        if template.name.matches('TabsDynamic'):
            i = 1
            while template.has('name' + str(i)):
                if template.get('name' + str(i)).value.strip() == 'Chromas':
                    print(i)
                    text = str(template.get('content' + str(i)).value.strip())
                    break
                i += 1
    matches = re.findall('\[\[Image:.+?\]\]', text)
    for match in matches:
        print(match)
        original_file_name = 'File:{}'.format(re.search('Image:(.+?)\|', match)[1])
        original_file = site.client.pages[original_file_name]
        if 'redirect' in original_file.text().lower():
            continue
        extension = re.search('[.](.*)', original_file_name)[1]
        new_name = re.search("\|([^|]*)\]\]", match)[1].strip("' ")
        if '}' in new_name:
            new_name = re.search('abbr\|([^|]*)', match)[1].strip("' ")
        print(new_name)
        if '=' in new_name or '{' in new_name or '}' in new_name or ':' in new_name or '/' in new_name:
            continue
        if 'Classic' in new_name:
            continue
        print(new_name)
        new_file = 'File:{}.{}'.format(new_name, extension)
        original_file.move(new_file)
