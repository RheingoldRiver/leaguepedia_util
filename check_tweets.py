import mwclient
import json
import tweepy
from datetime import date
import time
from dotenv import load_dotenv
import os

load_dotenv()
twitterapikey = os.getenv("apikey")
twitterapisecret = os.getenv("apisecret")

date = date.today()

def main():
	twitter_oauth = tweepy.OAuthHandler(twitterapikey, twitterapisecret)
	api = tweepy.API(twitter_oauth)

	site = mwclient.Site('lol.fandom.com', path='/')
	response = site.api('cargoquery',
		limit = "max",
		tables = "NewsItems=NI",
		fields = "NI.Source",
		where = 'NI.Source IS NOT NULL AND NI.Date_Sort = "{}"'.format(date)
	)
	parsed = json.dumps(response)
	data = json.loads(parsed)

	print("I have the data from the wiki!")

	exception = False

	for source in data["cargoquery"]:
		source = source["title"]["Source"].split(";")
		if source[6] == "twitter.com":
			splitStatus = source[0].split("/")
			try:
				r = api.get_status(splitStatus[5])
			except tweepy.NotFound as e:
				print("Tweet not found! {}".format(source[0]))
				exception = True
			except tweepy.TooManyRequests:
				time.sleep(10)

	if exception != True:
		print("Done! All tweets are available!")
	else:
		print("Done!")

if __name__ == '__main__':
    main()
