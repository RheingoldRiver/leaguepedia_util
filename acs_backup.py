import json
import re

from mwrogue.auth_credentials import AuthCredentials
from mwrogue.esports_client import EsportsClient

from lol_esports_parser.riot.acs_access import ACS


METADATA_PATTERN = """{{{{AcsMetadata
|RiotPlatformId={}
|RiotGameId={}
|RiotHash={}
|GameId={}
|MatchId={}
|N_GameInMatch={}
|OverviewPage={}
}}}}"""

credentials = AuthCredentials(user_file='bot')
site = EsportsClient('lol', credentials=credentials)
acs = ACS()

result = site.cargo_client.query(
    tables='MatchScheduleGame=MSG',
    fields='MatchHistory, GameId, OverviewPage, MatchId, N_GameInMatch',
    where='MatchHistory LIKE "%gameHash%"'
)


def get_metadata(row, realmx, game_idx, game_hashx):
    return METADATA_PATTERN.format(
        realmx,
        game_idx,
        game_hashx,
        row['GameId'],
        row['MatchId'],
        row['N GameInMatch'],
        row['OverviewPage']
    )


for game in result:
    re_match = re.match(r'^.*match-details/(.+?)/(.+?)\?gameHash=(.+?)(?:&tab=.*)?$', game['MatchHistory'])
    realm = re_match[1]
    game_id = re_match[2]
    game_hash = re_match[3]
    site.save_title('Acs:{}_{}'.format(realm, game_id), json.dumps(acs.get_game(realm, game_id, game_hash)))
    site.save_title('Acs:{}_{}/Timeline'.format(realm, game_id), json.dumps(acs.get_game_timeline(realm, game_id, game_hash)))
    site.save_title('Acs Metadata:{}_{}'.format(realm, game_id), get_metadata(game, realm, game_id, game_hash))
