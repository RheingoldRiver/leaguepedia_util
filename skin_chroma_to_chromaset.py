import time

from river_mwclient.esports_client import EsportsClient
from river_mwclient.auth_credentials import AuthCredentials
from river_mwclient.page_modifier import PageModifierBase
from mwparserfromhell.nodes.template import Template
from mwparserfromhell import parse

credentials = AuthCredentials(user_file="bot")
site = EsportsClient('lol', credentials=credentials)  # Set wiki
summary = 'Use ChromaSet'  # Set summary

param_lookup = {
	'': '1'
}

def add_param(new_chroma, tl, s, param):
	old_param = 'chroma' + s + param
	if not tl.has(old_param):
		return
	new_param = param_lookup[param] if param in param_lookup else param
	new_chroma.add(new_param, tl.get(old_param).value.strip())


def add_special_param(new_chroma, tl, s):
	old_param = 'special' + s
	if not tl.has(old_param):
		return
	special = tl.get(old_param).value
	for template in special.filter_templates():
		if template.name.matches('abbr'):
			new_chroma.add('special', template.get(2).value.strip())
			return
	new_chroma.add('special', special.strip())

class PageModifier(PageModifierBase):
	def update_plaintext(self):
		print('starting page ' + self.current_page.name)
		chromas = []
		price = ''
		release = ''
		template_list = self.current_wikitext.filter_templates()
		for infobox in template_list:
			infobox: Template
			if infobox.name.matches('ChromaSet'):
				self.current_wikitext.remove(infobox)
				self.current_text = str(self.current_wikitext)
				self.current_text = self.current_text.replace('== Chromas ==', '')
			if not infobox.name.matches('Infobox Skin'):
				continue
			if not infobox.has('chroma'):
				return
			if infobox.has('chroma_rp'):
				price = infobox.get('chroma_rp').value.strip()
			if infobox.has('chroma_date'):
				release = infobox.get('chroma_date').value.strip()
			param = infobox.get('chroma').value
			for tl in param.filter_templates():
				if not tl.name.matches('ChromaBox'):
					continue
				i = 1
				while tl.has('chroma' + str(i)):
					s = str(i)
					new_chroma = Template('ChromaSet/Line')
					add_param(new_chroma, tl, s, '')
					add_param(new_chroma, tl, s, 'hex1')
					add_param(new_chroma, tl, s, 'hex2')
					add_param(new_chroma, tl, s, 'name')
					add_param(new_chroma, tl, s, 'rp')
					add_special_param(new_chroma, tl, s)
					chromas.append(str(new_chroma))
					i += 1
		chroma_section = ['== Chromas ==', '{{{{ChromaSet|price={}|release={}'.format(price, release)]
		for chroma in chromas:
			chroma_section.append('|' + chroma)
		chroma_section.append('}}')
		self.current_text = self.current_text.replace(
			'{{ChampionSkinImageSections}}',
			'\n'.join(chroma_section) + '\n' + '{{ChampionSkinImageSections}}'
		)
		self.current_text = self.current_text.replace('\n\n\n', '\n')
		self.current_text = self.current_text.replace('\n\n', '\n')


PageModifier(site,
             page_list=site.pages_using('Infobox Skin'),
             summary=summary).run()
