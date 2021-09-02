import json
import re

from mwrogue.auth_credentials import AuthCredentials
from mwrogue.esports_client import EsportsClient

from lol_esports_parser.riot.acs_access import ACS
from requests import HTTPError

METADATA_PATTERN = """{{{{AcsMetadata
|RiotPlatformId={}
|RiotGameId={}
|RiotHash={}
|GameId={}
|MatchId={}
|N_GameInMatch={}
|OverviewPage={}
}}}}"""

credentials = AuthCredentials(user_file='me')
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

passed_startat = False
startat = 'ESPORTSTMNT02 1271211'

for game in result:
    re_match = re.match(r'^.*match-details/(.+?)/(.+?)\?gameHash=(.+?)(?:&a?m?p?;?tab=.*)?$', game['MatchHistory'])
    realm = re_match[1]
    game_id = re_match[2]
    game_hash = re_match[3]
    fingerprint = '{} {}'.format(realm, game_id)
    if fingerprint == startat:
        passed_startat = True
    if not passed_startat:
        continue
    print('Processing {} now, hash is {}...'.format(fingerprint, game_hash))
    try:
        site.save_title('V4 data:{}_{}'.format(realm, game_id), json.dumps(acs.get_game(realm, game_id, game_hash)))
    except HTTPError:
        with open('acs_errors.txt', 'a') as f:
            f.write('\n{} {} {}'.format(realm, game_id, game_hash))
        continue
    site.save_title('V4 data:{}_{}/Timeline'.format(realm, game_id), json.dumps(acs.get_game_timeline(realm, game_id, game_hash)))
    site.save_title('V4 metadata:{}_{}'.format(realm, game_id), get_metadata(game, realm, game_id, game_hash))
