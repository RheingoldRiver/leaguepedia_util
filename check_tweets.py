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
        tables="NewsItems=NI",
        fields="NI.Source, NI._pageName=pageName, NI.N_LineInDate",
        where='NI.Source IS NOT NULL AND NI.Date_Sort >= "{}"'.format(checkfrom),
        order_by="NI.Date_Sort DESC"
    )

    for source in response:
        sourcelist = source["Source"].split(":::")
        datapage = source["pageName"]
        lineindate = source["N LineInDate"]
        for source in sourcelist:
            if not source:
                continue
            source = source.split(";;;")
            sourcelink = source[0]
            if source[2] == "twitter.com":
                tweet_id = re.search(r"status/([0-9]+)", sourcelink)[1]
                if not tweet_id:
                    site.log_error_content("Can't get tweet id", text="Link: {0}".format(sourcelink))
                try:
                    r = twitter_client.get_tweet(tweet_id)
                except tweepy.TooManyRequests:
                    time.sleep(30)
                    r = twitter_client.get_tweet(tweet_id)
                if not r.errors:
                    continue
                if r.errors[0]["title"] == "Tweet Not Found Error":
                    site.log_error_content(f"{datapage}",
                                           text=f" Link: {sourcelink} - Line {lineindate}")
                else:
                    site.log_error_content("Failure trying to get tweet",
                                           text="Tweet Link: {0}, Status Id: {1}, Error Title: {2}".format(
                                               str(sourcelink), str(tweet_id), str(r.errors[0]["title"])))

    site.report_all_errors("Deleted Tweets")


if __name__ == '__main__':
    main()
