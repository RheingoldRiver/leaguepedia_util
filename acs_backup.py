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



def get_metadata(row, realmx, game_idx, game_hashx):
    return METADATA_PATTERN.format(
        realmx,
        game_idx,
        game_hashx or '',
        row['GameId'].replace('&amp;', '&'),
        row['MatchId'].replace('&amp;', '&'),
        row['N_GameInMatch'],
        row['OverviewPage']
    )

def main():

    credentials = AuthCredentials(user_file='bot')
    site = EsportsClient('lol', credentials=credentials)
    acs = ACS()

    result = site.cargo_client.query(
        tables='MatchScheduleGame=MSG,AcsMetadata=ACS',
        join_on='MSG.GameId=ACS.GameId',
        fields='MSG.MatchHistory=MatchHistory, MSG.GameId=GameId, MSG.OverviewPage=OverviewPage, MSG.MatchId=MatchId, MSG.N_GameInMatch=N_GameInMatch, MSG._pageName=Page',
        where='MatchHistory LIKE "%matchhistory%" AND ACS.GameId IS NULL'
    )

    passed_startat = True
    startat = 'FRA1TMNT1 210419'

    for game in result:
        if 'gameHash' in game['MatchHistory']:
            re_match = re.match(r'^.*match-details/(.+?)/(.+?)\?gameHash=(.+?)(?:&a?m?p?;?tab=.*)?$', game['MatchHistory'])
            realm = re_match[1]
            game_id = re_match[2]
            game_hash = re_match[3]
        else:
            re_match = re.match(r'^.*match-details/(.+?)/([^/]*).*$', game['MatchHistory'])
            realm = re_match[1]
            game_id = re_match[2]
            game_hash = None
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
            print(game['MatchHistory'])
            print(game['Page'])
            continue
        try:
            site.save_title('V4 data:{}_{}/Timeline'.format(realm, game_id), json.dumps(acs.get_game_timeline(realm, game_id, game_hash)))
        except HTTPError:
            print(game['MatchHistory'])
            print(game['Page'])
            pass
        site.save_title('V4 metadata:{}_{}'.format(realm, game_id), get_metadata(game, realm, game_id, game_hash))

if __name__ == '__main__':
    main()
