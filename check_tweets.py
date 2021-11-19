import mwclient
import tweepy
from datetime import date, timedelta
from dotenv import load_dotenv
import os
import re

load_dotenv()
bearertoken = os.getenv("bearertoken")

yesterday = date.today() - timedelta(days=4)

def main():
	client = tweepy.Client(bearer_token=bearertoken)

	site = mwclient.Site('lol.fandom.com', path='/')
	response = site.api('cargoquery',
		limit = "max",
		tables = "NewsItems=NI",
		fields = "NI.Source",
		where = 'NI.Source IS NOT NULL AND NI.Date_Sort >= "{}"'.format(yesterday),
		order_by = "NI.Date_Sort DESC"
	)

	print("I have the data from the wiki!")

	for source in response["cargoquery"]:
		source = source["title"]["Source"].split(";")
		if source[6] == "twitter.com":
			splitStatus = re.search(r"status/([0-9]+)", source[0])
			if not splitStatus:
				print("Error with tweet {}".format(str(source[0])))
			try:
				r = client.get_tweet(splitStatus[1])
			except Exception as e:
				print("Error with tweet {}".format(str(source[0])))
				print(e)
				continue
			if not r.errors:
				continue
			if r.errors[0]["title"] == "Not Found Error":
				print("Not found! {}".format(str(source[0])))
			else:
				print("Error with tweet! {0} - {1}".format(str(r.errors[0]["title"]), str(source[0])))

	print("Done!")

if __name__ == '__main__':
    main()
