from river_mwclient.gamepedia_client import GamepediaClient
from river_mwclient.auth_credentials import AuthCredentials

credentials = AuthCredentials(user_file="me")
site = GamepediaClient('thealchemistcode', credentials=credentials)

for i in range(1, 50):
	site.client.pages["User:RheingoldRiver/Test"].append("hello world", summary="rate limit testing")