import json
import requests

# links
SCHEDULE = "https://esports-api.lolesports.com/persisted/gw/getSchedule?hl=en-US&leagueId={}"
NEXT = "https://esports-api.lolesports.com/persisted/gw/getSchedule?hl=en-US&leagueId={}&pageToken={}"
LEAGUES = "https://esports-api.lolesports.com/persisted/gw/getLeagues?hl=en-US"

# templates
START = """== {0} ==
{{{{SetPatch|patch= |disabled= |hotfix= |footnote=}}}}
{{{{MatchSchedule/Start|tab={0} |bestof={1} |shownname= }}}}\n"""
MATCH = """{{{{MatchSchedule|<!-- Do not change the order of team1 and team2!! -->|initialorder={initialorder}|team1={t1} |team2={t2} |team1score= |team2score= |winner=
|date={date} |time={time} |timezone={timezone} |dst={dst} |pbp= |color= |vodinterview= |with= |stream={stream} |reddit=
{games}
}}}}\n"""
BO1_GAMES = """|game1={{MatchSchedule/Game
|blue= |red= |winner= |ssel= |ff=
|mh=
|recap=
|vodpb=
|vodstart=
|vodpost=
|vodhl=
|vodinterview=
|with=
|mvp=
}}"""
BO2_GAMES = """|game1={{MatchSchedule/Game
|blue= |red= |winner= |ssel= |ff=
|mh=
|recap=
|vodpb=
|vodstart=
|vodpost=
|vodhl=
|vodinterview=
|with=
|mvp=
}}
|game2={{MatchSchedule/Game
|blue= |red= |winner= |ssel= |ff=
|mh=
|recap=
|vodpb=
|vodstart=
|vodpost=
|vodhl=
|vodinterview=
|with=
|mvp=
}}"""
BO3_GAMES = """|game1={{MatchSchedule/Game
|blue= |red= |winner= |ssel= |ff=
|mh=
|recap=
|vodpb=
|vodstart=
|vodpost=
|vodhl=
|vodinterview=
|with=
|mvp=
}}
|game2={{MatchSchedule/Game
|blue= |red= |winner= |ssel= |ff=
|mh=
|recap=
|vodpb=
|vodstart=
|vodpost=
|vodhl=
|vodinterview=
|with=
|mvp=
}}
|game3={{MatchSchedule/Game
|blue= |red= |winner= |ssel= |ff=
|mh=
|recap=
|vodpb=
|vodstart=
|vodpost=
|vodhl=
|vodinterview=
|with=
|mvp=
}}"""
BO5_GAMES = """|game1={{MatchSchedule/Game
|blue= |red= |winner= |ssel= |ff=
|mh=
|recap=
|vodpb=
|vodstart=
|vodpost=
|vodhl=
|vodinterview=
|with=
|mvp=
}}
|game2={{MatchSchedule/Game
|blue= |red= |winner= |ssel= |ff=
|mh=
|recap=
|vodpb=
|vodstart=
|vodpost=
|vodhl=
|vodinterview=
|with=
|mvp=
}}
|game3={{MatchSchedule/Game
|blue= |red= |winner= |ssel= |ff=
|mh=
|recap=
|vodpb=
|vodstart=
|vodpost=
|vodhl=
|vodinterview=
|with=
|mvp=
}}
|game4={{MatchSchedule/Game
|blue= |red= |winner= |ssel= |ff=
|mh=
|recap=
|vodpb=
|vodstart=
|vodpost=
|vodhl=
|vodinterview=
|with=
|mvp=
}}
|game5={{MatchSchedule/Game
|blue= |red= |winner= |ssel= |ff=
|mh=
|recap=
|vodpb=
|vodstart=
|vodpost=
|vodhl=
|vodinterview=
|with=
|mvp=
}}"""
END = "{{MatchSchedule/End}}\n"


def get_headers():
    api_key = "0TvQnueqKa5mxJntVWt0w4LpLfEkrV1Ta8rQBb9Z"  # Todo: Get API Key from website but probably not
    headers = {"x-api-key": api_key}
    return headers


def get_json(json_type, headers):
    request = requests.get(json_type, headers=headers)
    json_file = json.loads(request.text)
    return json_file


def get_all_jsons(first_json, league_id, headers):
    jsons = [first_json]
    next_token = filter_json(first_json, "data", "schedule", "pages", "newer")
    while next_token is not None:
        next_json = get_json(NEXT.format(league_id, next_token), headers)
        jsons.append(next_json)
        next_token = filter_json(next_json, "data", "schedule", "pages", "newer")
    return jsons


def get_league(league_name, headers):
    json_leagues = get_json(LEAGUES, headers)
    json_leagues = filter_json(json_leagues, "data", "leagues")
    league_dict = next((league_dict for league_dict in json_leagues if league_dict["name"] == league_name), None)
    league_id = league_dict["id"]
    return league_id


def filter_json(json_file, *args):
    new_json = json_file
    for arg in args:
        try:
            new_json = new_json[arg]
        except KeyError:
            print("Couldn't find '{}'. Original json returned.".format(arg))
            return json_file
    return new_json


def parse_schedule(jsons, timezone="CET", dst="no", stream=""):
    initialorder = 1
    schedule, current_tab = "", ""
    for json_file in jsons:
        json_schedule = filter_json(json_file, "data", "schedule", "events")
        for game in json_schedule:
            date_time = game["startTime"]
            date = date_time[:10]
            time = date_time[11:16]
            display = game["blockName"]
            team1 = game["match"]["teams"][0]["name"]
            team2 = game["match"]["teams"][1]["name"]
            bestof = game["match"]["strategy"]["count"]
            if display != current_tab:
                schedule = schedule + START.format(display, bestof)
                current_tab = display
                initialorder = 1
            if bestof == 1:
                schedule = schedule + MATCH.format(initialorder=initialorder, t1=team1, t2=team2, date=date, time=time,
                                                   timezone=timezone, dst=dst, stream=stream, games=BO1_GAMES)
            elif bestof == 2:
                schedule = schedule + MATCH.format(initialorder=initialorder, t1=team1, t2=team2, date=date, time=time,
                                                   timezone=timezone, dst=dst, stream=stream, games=BO2_GAMES)
            elif bestof == 3:
                schedule = schedule + MATCH.format(initialorder=initialorder, t1=team1, t2=team2, date=date, time=time,
                                                   timezone=timezone, dst=dst, stream=stream, games=BO3_GAMES)
            elif bestof == 5:
                schedule = schedule + MATCH.format(initialorder=initialorder, t1=team1, t2=team2, date=date, time=time,
                                                   timezone=timezone, dst=dst, stream=stream, games=BO5_GAMES)
            else:
                # Todo: Throw an exception or something
                schedule = schedule + MATCH.format(initialorder=initialorder, t1=team1, t2=team2, date=date, time=time,
                                                   timezone=timezone, dst=dst, stream=stream, games=BO1_GAMES)
            initialorder += 1
    schedule = schedule + END
    return schedule


def run(league_name):
    headers = get_headers()
    league_id = get_league(league_name, headers)
    json_schedule = get_json(SCHEDULE.format(league_id), headers)
    jsons = get_all_jsons(json_schedule, league_id, headers)
    schedule = parse_schedule(jsons)
    return schedule


print(run("LCS"))
