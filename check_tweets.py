from mwrogue.esports_client import EsportsClient
from mwrogue.esports_client import AuthCredentials
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
	twitter_client = tweepy.Client(bearer_token=bearertoken)
	credentials = AuthCredentials(user_file="me")
	site = EsportsClient("lol", credentials=credentials)

	response = site.cargo_client.query(
		limit = "max",
		tables = "NewsItems=NI",
		fields = "NI.Source, NI._pageName=pageName, NI.N_LineInDate",
		where = 'NI.Source IS NOT NULL AND NI.Date_Sort >= "{}"'.format(checkfrom),
		order_by = "NI.Date_Sort DESC"
	)

	for source in response:
		sourcelist = source["Source"].split(":::")
		datapage = source["pageName"]
		lineindate = source["N LineInDate"]
		for source in sourcelist:
			if not source:
				continue
			source = source.split(";;;")
			if source[2] == "twitter.com":
				splitStatus = re.search(r"status/([0-9]+)", source[0])[1]
				if not splitStatus:
					site.log_error_content("\nCan't get tweet id for: {1}".format(source[0]))
				try:
					r = twitter_client.get_tweet(splitStatus)
				except tweepy.TooManyRequests:
					time.sleep(30)
					r = twitter_client.get_tweet(splitStatus)
				if not r.errors:
					continue
				elif r.errors[0]["title"] == "Not Found Error":
					site.log_error_content("\nTweet link: {0} Data page: {1} - Line {2}".format(str(source[0]), str(datapage), str(lineindate)))
				else:
					site.log_error_content("\nFailure when trying to get {0}, Error Title: {1}".format(str(source[0]), str(r.errors[0]["title"])))

	site.report_all_errors("Deleted Tweets")

if __name__ == '__main__':
    main()
