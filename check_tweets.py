import os
import re
import time
from datetime import date, timedelta

import tweepy
from mwrogue.esports_client import AuthCredentials
from mwrogue.esports_client import EsportsClient

check_from_date = date.today() - timedelta(days=4)

TWEET_NOT_FOUND_ERROR = "Not Found Error"


def main():
    twitter_client = tweepy.Client(bearer_token=os.environ.get('TWITTER_API_KEY'))
    credentials = AuthCredentials(user_file="me")
    site = EsportsClient("lol", credentials=credentials)

    response = site.cargo_client.query(
        tables="NewsItems=NI",
        fields="NI.Source, NI._pageName=pageName, NI.N_LineInDate",
        where='NI.Source IS NOT NULL AND NI.Date_Sort >= "{}"'.format(check_from_date),
        order_by="NI.Date_Sort DESC"
    )

    for item in response:
        source_list = item["Source"].split(":::")
        data_page = item["pageName"]
        line_in_date = item["N LineInDate"]
        for source_string in source_list:
            if not source_string:
                continue
            source = source_string.split(";;;")
            link = source[0]
            if source[2] != "twitter.com":
                continue

            # now we definitely have an existing source that's definitely from twitter
            tweet_id = re.search(r"status/([0-9]+)", link)[1]
            if not tweet_id:
                site.log_error_content("Can't get tweet id", text="Link: {0}".format(link))
                continue
            try:
                r = twitter_client.get_tweet(tweet_id)
            except tweepy.TooManyRequests:
                time.sleep(30)
                r = twitter_client.get_tweet(tweet_id)
            
            if not r.errors:
                continue
            if r.errors[0]["title"] == TWEET_NOT_FOUND_ERROR:
                site.log_error_content(f"{data_page}",
                                       text=f"Tweet not found! Link: {link} - Line {line_in_date}")
            else:
                site.log_error_content("Failure trying to get tweet",
                                       text="Other error! Link: {0}, Status Id: {1}, Error title: {2}".format(
                                           str(link), str(tweet_id), str(r.errors[0]["title"])))

    site.report_all_errors("Deleted Tweets")


if __name__ == '__main__':
    main()
