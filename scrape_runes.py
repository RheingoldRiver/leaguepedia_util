import re
import json
import urllib.request
import urllib.error
import math
import copy
import requests

from river_mwclient.esports_client import EsportsClient
from river_mwclient.auth_credentials import AuthCredentials

from lol_esports_parser.parsers.riot.acs_access import get_id_token

SILENT = True


def print_if_not_silent(str):
    if not SILENT:
        print(str)


def get_patch():
    with urllib.request.urlopen('http://ddragon.leagueoflegends.com/api/versions.json') as url:
        data = json.loads(url.read().decode())
        return data[0]


def get_rune_dict():
    patch = get_patch()
    with urllib.request.urlopen(
            'http://ddragon.leagueoflegends.com/cdn/{}/data/en_US/runesReforged.json'.format(patch)) as url:
        data = json.loads(url.read().decode())
    rune_dict = {
        5008: 'Adaptive Force',
        5007: 'Scaling CDR',
        5005: 'Attack Speed',
        5003: 'Magic Resist',
        5002: 'Armor',
        5001: 'Scaling Health',
        8000: 'Precision',
        8100: 'Domination',
        8200: 'Sorcery',
        8300: 'Inspiration',
        8400: 'Resolve',
        8358: 'MasterKey',
        'trees': {}
    }
    for tree in data:  # tree as in rune tree
        for slot in tree['slots']:
            for rune in slot['runes']:
                rune_dict[rune['id']] = rune['name']
                rune_dict['trees'][int(rune['id'])] = tree['key']
    return rune_dict


def get_champ_dict():
    patch = get_patch()
    champ_dict = {}
    with urllib.request.urlopen(
            'http://ddragon.leagueoflegends.com/cdn/{}/data/en_US/champion.json'.format(patch)) as url:
        champ_list = json.loads(url.read().decode())
    for champ in champ_list['data']:
        n = int(champ_list['data'][champ]['key'])
        champ_dict[n] = champ
    return champ_dict


def scrape(esc: EsportsClient, events, force):
    player_data_keys = ["perkPrimaryStyle", "perkSubStyle", "perk0", "perk1", "perk2", "perk3", "perk4", "perk5",
                        "statPerk0", "statPerk1", "statPerk2"]
    player_positions = ['Top', 'Jungle', 'Mid', 'ADC', 'Support']
    rune_dict = get_rune_dict()
    champ_dict = get_champ_dict()
    print_if_not_silent(events)
    with open('mh_riot_endpoint.txt') as f:
        mh_riot_endpoint = f.read().strip()
    mh_riot_token = get_id_token()
    for page_to_query in events:
        print_if_not_silent(page_to_query)
        result = esc.client.api('cargoquery', format="json",
                                limit='max',
                                tables="MatchScheduleGame=MSG,MatchSchedule=MS",
                                fields="MSG.OverviewPage,MSG.MatchHistory",
                                where=(r'MSG._pageName="%s" AND MSG.MatchHistory IS NOT NULL'
                                       r' AND NOT MSG.MatchHistory RLIKE ".*(lpl|lol)\.qq\.com.*"') % page_to_query,
                                join_on="MSG.UniqueMatch=MS.UniqueMatch",
                                order_by="MS.N_Page,MS.N_MatchInPage, MSG.N_GameInMatch"
                                )
        if result['cargoquery']:
            event = result['cargoquery'][0]['title']['OverviewPage']
            suffix = ''
            page_start = page_to_query.replace('Data:', '')
            if page_start != event:
                suffix = page_start.replace(event, '')
            errors_http = []
            errors_key = []
            page_name = event + '/Runes' + suffix
            page = esc.client.pages[page_name]
            text = page.text()
            text_tbl = []
            if text != "":
                text_tbl = text.split('\n')
                intro = text_tbl.pop(0) + '\n' + text_tbl.pop(0)
            else:
                overview_page = esc.client.pages[event]
                overview_text = overview_page.text()
                overview_text_tbl = overview_text.split('\n')
                tabs = overview_text_tbl[0]
                intro = tabs + '\n{{RunesStart2019}}'
            lines = [intro]
            for i, cargo_game in enumerate(result['cargoquery']):
                mh = (cargo_game['title']['MatchHistory']).replace('&amp;', '&')
                print_if_not_silent(mh)
                location = re.match(r'.*details/([^&]*)', mh)[1]
                if len(text_tbl) > 10 * i and (location in text_tbl[10 * i]) and not force:
                    for j in range(0, 10):
                        lines.append(text_tbl[j + 10 * i])
                else:
                    print_if_not_silent('Querying match %s' % mh)
                    json_loc = mh_riot_endpoint + location
                    try:
                        game = requests.Session().get(
                            json_loc,
                            cookies={
                                'id_token': mh_riot_token
                            }
                        ).json()
                        full_patch = game['gameVersion']
                        patch_tbl = full_patch.split('.')
                        patch = str(patch_tbl[0] + '.' + patch_tbl[1])
                        for j in range(0, 10):
                            player_name = game['participantIdentities'][j]['player']['summonerName']
                            try:
                                player_team = re.match('^(.+?) (.*)', player_name)[1]
                                player_name = re.match('^(.+?) (.*)', player_name)[2]
                            except Exception:
                                player_team = ''
                            player_champion_n = game['participants'][j]['championId']
                            player_champion = champ_dict.get(player_champion_n, str(player_champion_n))
                            player_position = player_positions[j % 5]
                            this_player = [player_name, player_team, player_champion, player_position]
                            for key in player_data_keys:
                                rune_key = game['participants'][j]['stats'][key]
                                rune_output = rune_dict.get(rune_key, rune_key)
                                this_player.append(rune_output)
                            this_player_output = '{{RunesLine2019|' + (
                                '|'.join(this_player)) + '|patch=' + patch + '|mh=' + location + '}}'
                            lines.append(this_player_output)
                            text_tbl.insert(10 * i + j, '')
                    except urllib.error.HTTPError:
                        errors_http.append(mh)
                    except KeyError:
                        errors_key.append(mh)
            lines.append('{{RunesEnd}}')
            new_text = '\n'.join(lines)
            if new_text != text and len(lines) > 3:
                print_if_not_silent('Saving page %s...' % page_name)
                esc.save(page, new_text, summary='Automatically updating Runes (python)')
            else:
                print_if_not_silent('Skipping page %s, no changes' % page_name)
            error_text = ''
            for e in errors_http:
                error_text = error_text + ' <br>\n' + page_to_query + ': ' + e + ' (HTTP)'
            for e in errors_key:
                error_text = error_text + '\n' + e + ' (Key)'
            if error_text != '':
                error_page = esc.client.pages['User:RheingoldRiver/Rune Errors']
                esc.save(error_page, error_text, summary='Reporting a Rune Error')


def get_player_data(game, team_keys, j):
    team_key = team_keys[math.floor(j / 5)]
    player_key = j % 5
    return game[team_key]['players'][player_key]


def get_team_names(game):
    str = game['msg']['sMatchInfo']['bMatchName']
    arr = str.split(' ')
    blue = game['msg']['sMatchInfo']['BlueTeam']
    teamA = game['msg']['sMatchInfo']['TeamA']
    teamB = game['msg']['sMatchInfo']['TeamB']
    if blue == teamA:
        return {'left': arr[0], 'right': arr[2]}
    elif blue == teamB:
        return {'left': arr[2], 'right': arr[0]}


def get_this_teamname(teamnames, team_keys, j):
    team_key = team_keys[math.floor(j / 5)]
    return teamnames[team_key]


def scrapeLPL(esc: EsportsClient, events, force):
    player_positions = ['Top', 'Jungle', 'Mid', 'ADC', 'Support']
    rune_dict = get_rune_dict()
    champ_dict = get_champ_dict()
    please_escape = False
    with open('mh_qq_endpoint.txt') as f:
        mh_qq_endpoint = f.readlines()
    mh_qq_endpoint = [_.strip() for _ in mh_qq_endpoint]
    for page_to_query in events:
        if please_escape:
            break
        print_if_not_silent(page_to_query)
        result = esc.client.api('cargoquery', format="json",
                                limit='max',
                                tables="MatchScheduleGame=MSG,MatchSchedule=MS",
                                fields="MSG.OverviewPage,MSG.MatchHistory",
                                where=(r'MSG._pageName="%s" AND MSG.MatchHistory IS NOT NULL'
                                       r' AND MSG.MatchHistory RLIKE ".*(lpl|lol)\.qq\.com.*"') % page_to_query,
                                join_on="MSG.UniqueMatch=MS.UniqueMatch",
                                order_by="MS.N_Page,MS.N_MatchInPage, MSG.N_GameInMatch",
                                group_by='MSG.MatchHistory'
                                )
        if not result['cargoquery']:
            continue
        event = result['cargoquery'][0]['title']['OverviewPage']
        suffix = ''
        page_start = page_to_query.replace('Data:', '')
        if page_start != event:
            suffix = page_start.replace(event, '')
        errors_http = []
        errors_key = []
        page_name = event + '/Runes' + suffix
        page = esc.client.pages[page_name]
        text = page.text()
        text_tbl = []
        team_keys = ['left', 'right']
        if text != "":
            text_tbl = text.split('\n')
            intro = text_tbl.pop(0) + '\n' + text_tbl.pop(0)
        else:
            overview_page = esc.client.pages[event]
            overview_text = overview_page.text()
            overview_text_tbl = overview_text.split('\n')
            tabs = overview_text_tbl[0]
            intro = tabs + '\n{{RunesStart2019}}'
        lines = [intro]
        counter = 0
        for i, cargo_game in enumerate(result['cargoquery']):
            # lmt += 1
            # if lmt == 2:
            # 	please_escape = True
            # 	break
            mh = (cargo_game['title']['MatchHistory']).replace('&amp;', '&')
            print_if_not_silent(mh)
            location = re.match(r'.*bmid=([0-9]*)', mh)[1]
            if len(text_tbl) > 10 * counter and (location in text_tbl[10 * counter]) and not force:
                print_if_not_silent('Skipping %s' % location)
                for j in range(0, 10):
                    lines.append(text_tbl[j + 10 * counter])
                counter = counter + 1
                if len(text_tbl) > 10 * counter and (location in text_tbl[10 * counter]) and not force:
                    print_if_not_silent('Skipping %s (2)' % location)
                    for j in range(0, 10):
                        lines.append(text_tbl[j + 10 * counter])
                    counter = counter + 1
                    if len(text_tbl) > 10 * counter and (location in text_tbl[10 * counter]) and not force:
                        print_if_not_silent('Skipping %s (3)' % location)
                        for j in range(0, 10):
                            lines.append(text_tbl[j + 10 * counter])
                        counter = counter + 1
            else:
                print_if_not_silent('Querying match %s' % mh)
                json_loc = mh_qq_endpoint[0] + location
                print_if_not_silent(json_loc)
                try:
                    with urllib.request.urlopen(json_loc) as url:
                        series = json.loads(url.read().decode())
                    for game in series['msg']:
                        counter = counter + 1
                        gameId = game['sMatchId']
                        json_loc_2 = mh_qq_endpoint[1] + gameId
                        print_if_not_silent(json_loc_2)
                        with urllib.request.urlopen(json_loc_2) as url:
                            game = json.loads(url.read().decode())
                        areaId = game['msg']['sMatchInfo']['AreaId']
                        battleId = game['msg']['battleInfo']['BattleId']
                        json_loc_3 = mh_qq_endpoint[2] + battleId + mh_qq_endpoint[3] + areaId
                        print_if_not_silent(json_loc_3)
                        with urllib.request.urlopen(json_loc_3) as url:
                            worldLookup = json.loads(url.read().decode())
                        worldLookupJSON = json.loads(worldLookup['msg'])
                        has_runes = True
                        rune_data = {}
                        if worldLookupJSON['battle_count_'] == 0:
                            has_runes = False
                        else:
                            worldId = worldLookupJSON['battle_list_'][0]['world_']
                            json_loc_4 = mh_qq_endpoint[4] + str(worldId) + mh_qq_endpoint[5] + str(battleId)
                            print_if_not_silent(json_loc_4)
                            with urllib.request.urlopen(json_loc_4) as url:
                                rune_data_unsorted_init = json.loads(url.read().decode())
                            rune_data_unsorted = json.loads(rune_data_unsorted_init['msg'])
                            for p in range(0, 10):
                                rune_key = rune_data_unsorted['hero_list_'][p]['hero_id_']
                                rune_data[int(rune_key)] = rune_data_unsorted['hero_list_'][p].copy()
                        patch = ''  # unless we can automated get patch which idt we can from any endpoint
                        teamnames = get_team_names(game)
                        game_data = json.loads(game['msg']['battleInfo']['BattleData'])
                        j = 0
                        for j in range(0, 10):
                            rune_data_this = {}
                            if has_runes:
                                rune_data_this = copy.deepcopy(rune_data)
                            player_data = get_player_data(game_data, team_keys, j)
                            player_champion_n = int(player_data['hero'])
                            player_name = player_data['name']
                            player_team = get_this_teamname(teamnames, team_keys, j)
                            player_name = player_name.replace(player_team, '')
                            player_champion = champ_dict[player_champion_n] if player_champion_n in champ_dict else str(
                                player_champion_n)
                            player_position = player_positions[j % 5]
                            this_player = [player_name, player_team, player_champion, player_position]
                            if has_runes:
                                player_rune_data = rune_data_this[player_champion_n]['runes_info_'][
                                    'runes_list_'].copy()
                                this_rune_id = ''
                                this_player.append(rune_dict['trees'][player_rune_data[0]['runes_id_']])
                                for _ in range(0, 5):
                                    this_rune = player_rune_data.pop(0)
                                    this_rune_id = this_rune['runes_id_']
                                    rune_output = rune_dict[this_rune_id] if this_rune_id in rune_dict else this_rune_id
                                    this_player.append(rune_output)
                                this_player.insert(5, rune_dict['trees'][int(this_rune_id)])
                                stat_runes = player_rune_data.copy()
                                while stat_runes:
                                    if stat_runes[0]['runes_num_'] == 1:
                                        this_rune = stat_runes.pop(0)
                                    else:
                                        this_rune = stat_runes[0]
                                        stat_runes[0]['runes_num_'] = stat_runes[0]['runes_num_'] - 1
                                    this_rune_id = this_rune['runes_id_']
                                    rune_output = rune_dict[this_rune_id] if this_rune_id in rune_dict else this_rune_id
                                    this_player.append(rune_output)
                            this_player_output = '{{RunesLineLPL2019|' + (
                                '|'.join(this_player)) + '|patch=' + patch + '|mh=' + location + '}}'
                            lines.append(this_player_output)
                        text_tbl.insert(10 * i + j, '')
                except urllib.error.HTTPError:
                    errors_http.append(mh)
                except KeyError:
                    errors_key.append(mh)
                except Exception as e:
                    print_if_not_silent(e)
        lines.append('{{RunesEnd}}')
        new_text = '\n'.join(lines)
        if new_text != text and len(lines) > 3:
            print_if_not_silent('Saving page %s...' % page_name)
            esc.save(page, new_text, summary='Automatically updating Runes (python)')
        else:
            print_if_not_silent('Skipping page %s, no changes' % page_name)
        error_text = ''
        for e in errors_http:
            error_text = error_text + ' <br>\n' + page_to_query + ': ' + e + ' (HTTP)'
        for e in errors_key:
            error_text = error_text + '\n' + e + ' (Key)'
        if error_text != '':
            error_page = esc.client.pages['User:RheingoldRiver/Rune Errors']
            esc.save(error_page, error_text, summary='Reporting a Rune Error')


if __name__ == '__main__':
    SILENT = False
    credentials = AuthCredentials(user_file="me")
    esc_main = EsportsClient('lol', credentials=credentials)  # Set wiki
    pages = ['Data:Prime League Pro Division/2021 Season/Spring Promotion']
    scrape(esc_main, pages, False)
    # scrapeLPL(esc_main, pages, False)
