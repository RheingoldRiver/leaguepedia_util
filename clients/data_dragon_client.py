import requests
import re, json, urllib.request, urllib.error, math, copy

class DataDragonClient:
    """
    Super simple class to help search for artifacts within Nexus.
    In the future, we can increase the level of abstraction,
    and have this class do more of the heavy lifting.
    """
    # https://stackoverflow.com/a/16511493
    def getData(self, url):
        try:
            res = requests.get(url)
            res.raise_for_status()
        except requests.exceptions.RequestException as err:
            print('Generic error handling for Request Library.')
            print('API Request to Datadragon URL: ' + url + ' - Failed for error:')
            print(err)
        return res.json()

# Some boilerplate if we ever want to run classes like this straight from command line.
# python <filename>.py
if __name__ == '__main__':
    data_dragon_client = DataDragonClient()
    res = data_dragon_client.getData('https://ddragon.leagueoflegends.com/cdn/9.13.1/data/en_US/champion.json')
    print(res)
