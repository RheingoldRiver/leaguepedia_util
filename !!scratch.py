from river_mwclient.esports_client import EsportsClient
from river_mwclient.auth_credentials import AuthCredentials
from river_mwclient.template_modifier import TemplateModifierBase
from mwparserfromhell import parse

credentials = AuthCredentials(user_file="me")
site = EsportsClient('lol', credentials=credentials)
summary = 'Moving QQ links to outside of the games since they\'re for the entire series'


class TemplateModifier(TemplateModifierBase):
	def update_template(self, template):
		if template.has('qq'):
			return
		i = 1
		s = str(i)
		mh = None
		while template.has('game{}'.format(s)):
			game_text = template.get('game{}'.format(s)).value.strip()
			for tl in parse(game_text).filter_templates():
				if tl.name.matches('MatchSchedule/Game'):
					if not tl.has('mh'):
						continue
					mh = tl.get('mh').value.strip()
					if 'qq.com' in mh:
						break
					else:
						mh = None
			if mh is not None:
				break
			i += 1
			s = str(i)
		if mh is not None:
			template.add('qq', mh + '\n', before = 'game1')

TemplateModifier(site, 'MatchSchedule', recursive=False,
                 summary=summary).run()
