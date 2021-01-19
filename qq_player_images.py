import json
import os
from urllib.request import Request, urlopen, urlretrieve

PLAYER = "https://lpl.qq.com/web201612/data/LOL_MATCH2_TEAM_MEMBER{}_INFO.js"
TEAM = "https://lpl.qq.com/web201612/data/LOL_MATCH2_TEAM_TEAM{}_INFO.js"

LPL = [57, 1, 685, 7, 2, 29, 4, 9, 6, 11, 8, 422, 41, 42, 438, 587, 12]
LDL = [597, 602, 55, 595, 689, 109, 594, 688, 593, 603, 436, 687, 599, 433, 447, 444, 686, 28, 445, 592, 33, 598, 601, 56, 600, 596]


def _parse_page(page_id, page_type):
    url = Request(page_type.format(page_id))
    return json.load(urlopen(url))


def _filter_json(json_file, *args):
    new_json = json_file
    for arg in args:
        try:
            new_json = new_json[arg]
        except KeyError:
            print("Couldn't find '{}'. Original json returned.".format(arg))
            return json_file
    return new_json


def _get_value(json_file, key):
    try:
        return json_file[key]
    except KeyError:
        print("Couldn't find '{}'. Original json returned.".format(key))
        return json_file


def _download_images(player_name, team_name, season, link550px="", link250px=""):
    if link550px != "":
        filename = "{} {} {}.png".format(team_name, player_name, season)
        link = "https:{}".format(link550px)
        urlretrieve(link, "Player_Images/{}".format(filename))
    if link250px != "":
        filename250px = "250px_{} {} {}.png".format(team_name, player_name, season)
        link250px = "https:{}".format(link250px)
        urlretrieve(link250px, "Player_Images_250px/{}".format(filename250px))


def get_images(teams: list = None, season="", low_res=False):
    try:
        os.mkdir("Player_Images")
    except FileExistsError:
        pass
    if low_res:
        try:
            os.mkdir("Player_Images_250px")
        except FileExistsError:
            pass
    for team in teams:
        json_file = _parse_page(team, TEAM)
        players = _filter_json(json_file, "msg", "activePlayers")
        team_name = _filter_json(json_file, "msg", "baseInfo")
        team_name = _get_value(team_name, "TeamName")
        for player in players:
            player_id = _filter_json(player, "MemberId")
            player_page = _parse_page(player_id, PLAYER)
            player_data = _filter_json(player_page, "msg", "baseInfo")
            player_name = _get_value(player_data, "NickName")
            print(team_name, player_id, season)
            image550px = _get_value(player_data, "UserPhoto550")
            if low_res:
                image250px = _get_value(player_data, "UserIcon")
            else:
                image250px = ""
            _download_images(player_name, team_name, season, image550px, image250px)
