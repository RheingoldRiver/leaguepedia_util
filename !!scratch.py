from river_mwclient.esports_client import EsportsClient
from river_mwclient.auth_credentials import AuthCredentials
from river_mwclient.template_modifier import TemplateModifierBase

credentials = AuthCredentials(user_file="me")
site = EsportsClient('lol', credentials=credentials)  # Set wiki
summary = 'Clean up bundle/loot exclusive to their own args'  # Set summary


class TemplateModifier(TemplateModifierBase):
    def update_template(self):
        if not self.current_template.has('special'):
            return
        special = self.current_template.get('special').value.strip()
        if special == 'Loot Exclusive':
            self.current_template.add('loot_exclusive', 'Yes')
            self.current_template.remove('special')
        if special == 'Bundle Exclusive':
            self.current_template.add('bundle_exclusive', 'Yes')
            self.current_template.remove('special')


TemplateModifier(site, 'ChromaSet/Line',
                 summary=summary).run()
