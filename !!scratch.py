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

TABS = [ 'Splash Screens', 'Portraits', 'In-Game Screenshots', 'Concept Art' ]

for champion_page in site.client.categories['Champions']:
    champion = champion_page.name
    # if champion_page.name < 'Braum':
    #     continue
    print(champion)
    for tab in TABS:
        gallery_page = site.client.pages[champion + '/Gallery/{}'.format(tab)]
        text = gallery_page.text()
        wikitext = parse(text)
        sections = []
        for template in wikitext.filter_templates():
            template: Template
            if template.name.matches('TabsDynamic'):
                i = 1
                while template.has('name' + str(i)):
                    name = template.get('name' + str(i)).value.strip()
                    if re.search(name, 'nowrap'):
                        name = re.search('nowrap\|(\w+)', name)[1]
                    sections.append('== {} ==\n{}'.format(name, template.get('content' + str(i)).value.strip()))
                    i += 1
        if not sections:
            continue
        new_text = '{{ChampTabsHeader}}\n{{TOCFlat}}\n' + '\n'.join(sections)
        gallery_page.save(new_text, summary=summary)
