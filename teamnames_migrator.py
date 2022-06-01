import json
from mwrogue.esports_client import EsportsClient
from mwrogue.auth_credentials import AuthCredentials
from mwcleric.errors import RetriedLoginAndStillFailed
import re


class TeamnamesMigrator(object):
    DATA_PAGE = "{{{{Teamnames/Start}}}}\n{}{{{{Teamnames/End}}}}"
    TEAM_TEMPLATE = "{{{{Teamnames{}}}}}\n"

    def __init__(self, site):
        self.site = site
        self.processed_teamnames = {}
        self.exceptions = {}
        self.team_indexes = {}
        self.teamnames = {}

    def run(self):
        self.get_teamnames()
        self.process_teams()
        self.populate_inputs()
        self.make_output_and_save()

    def get_one_encoded_json(self, filename, mask):
        result = self.site.client.api(
            'expandtemplates',
            prop='wikitext',
            text='{{{{JsonEncode|{}|{}}}}}'.format(filename, mask)
        )
        return json.loads(result['expandtemplates']['wikitext'])

    def get_teamnames(self):
        dict1 = self.get_one_encoded_json("Team", "include_match=^[a-s].*")
        dict2 = self.get_one_encoded_json("Team", "exclude_match=^[a-s].*")

        self.teamnames = {**dict1, **dict2}

    def process_teams(self):
        for key, value in self.teamnames.items():
            if type(value) == dict:
                if value.get("exception"):
                    self.exceptions[key] = value
                    continue
                if value["link"].split(" ", 1)[0].lower() != "team":
                    first_letter = value["link"][0].upper()
                else:
                    first_letter = value["link"].split(" ", 1)[1][0].upper()
                    first_letter = f"Team {first_letter}"
                if not re.search("[A-Z0-9]", first_letter):
                    first_letter = "Other"
                if first_letter not in self.processed_teamnames.keys():
                    self.processed_teamnames[first_letter] = {}
                self.processed_teamnames[first_letter][key] = {
                    "inputs": [key],
                    "link": value["link"],
                    "long": value["long"],
                    "medium": value["medium"],
                    "short": value["short"],
                    "black": "true" if value.get("class") == "black" else "false",
                    "dark": "true" if value.get("class") == "dark" else "false"
                }
                self.team_indexes[key] = first_letter

    def populate_inputs(self):
        for key, value in self.teamnames.items():
            if isinstance(value, str):
                try:
                    self.processed_teamnames[self.team_indexes[value]][value]["inputs"].append(key)
                except KeyError:
                    self.exceptions[key] = value

    @staticmethod
    def concat_args(data):
        ret = ''
        lookup = data

        if type(data) == dict:
            lookup = []
            for k, v in data.items():
                lookup.append({k: v})

        for item in lookup:
            for key in item.keys():
                if isinstance(item[key], list):
                    ret += '|{}'.format(";".join(item[key]))
                    continue
                if item[key] is None:
                    ret = ret + '|{}='.format(key)
                else:
                    ret = ret + '|{}={}'.format(key, str(item[key]))

        return ret

    def make_output_and_save(self):
        for page, teams in self.processed_teamnames.items():
            page = f"Data:Teamnames/{page}"
            page_teams_output = ""
            for team in teams.values():
                page_teams_output += self.TEAM_TEMPLATE.format(self.concat_args(team))
            page_output = self.DATA_PAGE.format(page_teams_output)
            try:
                site.save_title(title=page, text=str(page_output), summary="Migrating Teamnames to Data")
            except RetriedLoginAndStillFailed:
                pass
            print(f"Saved {page}")


if __name__ == "__main__":
    credentials = AuthCredentials(user_file="me")
    site = EsportsClient("lol", credentials=credentials, max_retries_mwc=0, max_retries=0, retry_interval=0)
    TeamnamesMigrator(site).run()
