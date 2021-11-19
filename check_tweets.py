import mwclient
import tweepy
from datetime import date, timedelta
import time
from dotenv import load_dotenv
import os
import re

load_dotenv()
bearertoken = os.getenv("bearertoken")

checkfrom = date.today() - timedelta(days=4)

def main():
	client = tweepy.Client(bearer_token=bearertoken)

	site = mwclient.Site('lol.fandom.com', path='/')
	response = site.api('cargoquery',
		limit = "max",
		tables = "NewsItems=NI",
		fields = "NI.Source",
		where = 'NI.Source IS NOT NULL AND NI.Date_Sort >= "{}"'.format(checkfrom),
		order_by = "NI.Date_Sort DESC"
	)

	print("I have the data from the wiki!")

	for source in response["cargoquery"]:
		sourcelist = source["title"]["Source"].split(":::")
		for source in sourcelist:
			if not source:
				continue
			source = source.split(";;;")
			if source[2] == "twitter.com":
				splitStatus = re.search(r"status/([0-9]+)", source[0])[1]
				if not splitStatus:
					print("Error with tweet {}".format(str(source[0])))
				try:
					r = client.get_tweet(splitStatus)
				except tweepy.TooManyRequests:
					print("Ratelimited! Waiting 30 seconds")
					time.sleep(30)
					r = client.get_tweet(splitStatus)
				if not r.errors:
					continue
				elif r.errors[0]["title"] == "Not Found Error":
					print("Not found! {}".format(str(source[0])))
				else:
					print("Error with tweet! {0} - {1}".format(str(r.errors[0]["title"]), str(source[0])))

	print("Done!")

if __name__ == '__main__':
    main()
