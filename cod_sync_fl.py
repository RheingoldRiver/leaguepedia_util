from mwrogue.esports_client import EsportsClient
from mwcleric.auth_credentials import AuthCredentials
from mwcleric.wiki_client import WikiClient
from mwparserfromhell.nodes import Template
import mwparserfromhell

credentials = AuthCredentials(user_file="me")
cod_wiki = EsportsClient('cod-esports', credentials=credentials)
target_wiki = WikiClient(url='https://river-sandbox.fandom.com', path='/', credentials=credentials)
summary = 'Bot edit'

fl_page = cod_wiki.client.pages['Call of Duty Esports Wiki:Featured Leagues/Call of Duty League/2021 Season']
fl_page_text = fl_page.text()
template_text = None
for template in mwparserfromhell.parse(fl_page_text).filter_templates():
	template: Template
	if template.name.matches('Standings'):
		template_text = str(template)
		break
parsed_text_result = cod_wiki.client.api('expandtemplates',
                                  prop='wikitext',
                                  text=template_text
                                  )
parsed_text = parsed_text_result['expandtemplates']['wikitext']

parsed_text = parsed_text.replace('wikitable2', 'wikitable')

target_wiki.client.pages['testcodfl'].save(parsed_text)
