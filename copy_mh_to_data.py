import mwparserfromhell
from mwrogue.esports_client import EsportsClient
from mwrogue.auth_credentials import AuthCredentials

credentials = AuthCredentials(user_file="me")
site = EsportsClient("lol", credentials=credentials)

finished = False

fullresponse = []
offset = 0

while finished != True:
    response = site.cargo_client.query(
        limit = "max",
	    tables = "MatchScheduleGame=MSG, ScoreboardGames=SG",
        offset = offset,
        join_on= "MSG.GameId=SG.GameId",
	    fields = ["MSG.GameId", "SG.GameId",
        "MSG.MatchHistory", "SG.MatchHistory",
        "MSG._pageName=DataPage", "SG._pageName=SBPage",
        "MSG.N_MatchInTab", "MSG.N_TabInPage", "MSG.N_GameInMatch"],
        where = "MSG.MatchHistory IS NULL AND SG.MatchHistory IS NOT NULL AND SG._pageName IS NOT NULL AND MSG._pageName IS NOT NULL",
        order_by = "DataPage"
    )
    if len(response) != 500 or not response:
        finished = True
    offset += 500
    fullresponse += response
    
for item in fullresponse:
    if "matchhistory" not in item["MatchHistory"]:
        continue
    MatchInTab = item["N MatchInTab"]
    TabInPage = item["N TabInPage"]
    GameInMatch = item["N GameInMatch"]
    data_page = site.client.pages[item["DataPage"]]
    data_text = data_page.text()
    data_wikitext = mwparserfromhell.parse(data_text)
    timesfoundtab = 0
    timesfoundmatch = 0
    for template in data_wikitext.filter_templates():
        if template.name.strip() != "MatchSchedule/Start":
            if template.name.strip() != "MatchSchedule":
                continue
            elif timesfoundtab != TabInPage:
                continue
            else:
                timesfoundmatch += 1
        elif timesfoundtab != TabInPage:
            timesfoundtab += 1
            continue
        if timesfoundmatch == MatchInTab and timesfoundtab == TabInPage:
            print(template)
            break

#if str(data_wikitext) != data_text:
#		data_page.save(str(data_wikitext), summary = "Adding MH")
