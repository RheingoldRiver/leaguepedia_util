from bs4 import BeautifulSoup
from datetime import datetime
import pytz
import requests

# Change this for your specific tournament
schedule_url = "https://elements.lvp.global/wp-admin/admin-ajax.php?action=multi_calendar_template_callback&selectedCompetition=d7370dbe-d26b-11ec-9e84-06f414ba766d"
shownname = "LMF 2022 Closing"
stream = "https://twitch.tv/lvparg"

# To be used when matches in the same week are not in the same calendar week, so the script puts the matches separately
"""
Example:
tabs = {
    "JORNADA 1": "Week 1",
    "JORNADA 3": "Week 3"
}
"""
tabs = {
}

# This parser can't automatically get how many games are in a match, the default value will be 1
"""
Example:
tabs_bestof = {
    ("JORNADA 1", 2): 5
}
The second match of JORNADA 1 is Best of 5
tabs_bestof = {
    ("JORNADA 1", 0): 5
}
All matches in JORNADA 1 are Best of 5
tabs_bestof = {
    (0, 0): 5
}
All matches are Best of 5

If you input that all matches are Best of 5 but also one tab is for example Best of 3, that should work
"""
tabs_bestof = {
}

# Sometimes teams in the schedule page are not a valid input in Leaguepedia, you may put them below
"""
Example:
team_names = {
    "BANDITS": "Bandits Gaming"
}
The team name is BANDITS in LVP's page, it will be converted to Bandits Gaming in the output schedule
"""
team_names = {
}

html = requests.get(schedule_url).text

START = """== {0} ==
{{{{SetPatch|patch= |disabled= |hotfix= |footnote=}}}}
{{{{MatchSchedule/Start|tab={0} |bestof={1} |shownname={2} }}}}\n"""
MATCH = """{{{{MatchSchedule|bestof={best_of} |team1={t1} |team2={t2} |team1score= |team2score= |winner=
|date={date} |time={time} |timezone={timezone} |dst={dst} |pbp= |color= |vodinterview= |with= |stream={stream} |mvp=
{games}}}}}\n"""
GAME = """|game{}={{{{MatchSchedule/Game\n|blue= |red= |winner= |ssel= |ff=\n|riot_platform_game_id=\n|recap=\n|vodpb=
|vodstart=\n|vodpost=\n|vodhl=\n|vodinterview=\n|with=\n}}}}\n"""
END = "{{MatchSchedule/End}}\n\n"

parsed_html = BeautifulSoup(html, "html.parser")
page = parsed_html.find_all("div", "calendar-item")
title = ""
schedule = ""
current_week = -1
title_week = 0

for item in page:
    matches = item.find_all("div", class_="match-result-container")
    web_title = item.find("span", class_="result-round-title").text
    match_in_tab = 0
    for match in matches:
        match_in_tab += 1
        start_timestamp = int(match.find("usertime").text)
        start_datetime = datetime.fromtimestamp(start_timestamp)
        start_week = start_datetime.isocalendar()[1]
        if tabs_bestof.get((web_title, match_in_tab)):
            best_of = tabs_bestof[(web_title, match_in_tab)]
        elif tabs_bestof.get((web_title, 0)):
            best_of = tabs_bestof[(web_title, 0)]
        elif tabs_bestof.get((0, 0)):
            best_of = tabs_bestof[(0, 0)]
        else:
            best_of = 1
        if current_week != start_week:
            current_week = start_week
            title_week += 1
            title = tabs.get(web_title) or f"Week {title_week}"
            schedule = schedule + END + START.format(title, best_of, shownname)
        local = match.find("div", class_="local-container").find("span").text
        if team_names.get(local):
            local = team_names[local]
        visitor = match.find("div", class_="visitor-container").find("span").text
        if team_names.get(visitor):
            visitor = team_names[visitor]
        pst_object = start_datetime.astimezone(pytz.timezone("PST8PDT"))
        if pst_object.dst():
            dst = "spring"
        else:
            dst = "no"
        start_date = pst_object.strftime("%Y-%m-%d")
        start_time = pst_object.strftime("%H:%M")
        games = ""
        for gamen in range(best_of):
            gamen += 1
            games += GAME.format(gamen)
        schedule = schedule + MATCH.format(t1=local, t2=visitor, date=start_date, time=start_time, timezone="PST",
                                           dst=dst, stream=stream, games=games, best_of=best_of)

schedule = schedule.replace("{{MatchSchedule/End}}\n\n", "", 1)
schedule = schedule + END

print(schedule)
