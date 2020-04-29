import re
from river_mwclient.esports_client import EsportsClient
from river_mwclient.auth_credentials import AuthCredentials
from river_mwclient.template_modifier import TemplateModifierBase
from river_mwclient.page_modifier import PageModifierBase
from mwparserfromhell import parse
from mwparserfromhell.nodes.template import Template

credentials = AuthCredentials(user_file="me")
site = EsportsClient('valorant', credentials=credentials)  # Set wiki
summary = 'Move round totals to actual rounds param'  # Set summary

class TemplateModifier(TemplateModifierBase):
    def update_template(self):
        template = self.current_template
        if not (template.has('team1score') and template.has('team2score')):
            return
        if template.get('team1score').value.strip() == '':
            return
        if template.get('team2score').value.strip() == '':
            return
        rounds1 = int(template.get('team1score').value.strip())
        rounds2 = int(template.get('team2score').value.strip())
        if rounds1 != 13 and rounds2 != 13:
            return
        template.add('team1rounds', rounds1, before="team1score")
        template.add('team2rounds', rounds2, before="team2score")
        if rounds1 == 13:
            template.add('team1score', 1)
            template.add('team2score', 0)
        elif rounds2 == 13:
            template.add('team2score', 1)
            template.add('team1score', 0)

TemplateModifier(site, 'MatchSchedule',
                 # title_list=['Data:100 Thieves Invitational 2020'],
                 summary=summary).run()
