import asyncio
import datetime
import json
import time
from json.decoder import JSONDecodeError

import aiohttp
import backoff
import pytz
from mwcleric.auth_credentials import AuthCredentials
from mwrogue.esports_client import EsportsClient

GCD_URL = "https://spreadsheets.google.com/feeds/cells/1Y7k5kQ2AegbuyiGwEPsa62e883FYVtHqr6UVut9RC4o/{}/public/values?alt=json"

ARCHIVE_INTRO = '<noinclude>{{{{GCDBackup|lastupdateddate={}|lastupdatedtime={}|pagecreationdate={}|pagecreationtime={}}}}}</noinclude>\n'

CURRENT_INTRO = '<noinclude>{{GCDBackupCurrent}}</noinclude>\n'

GCD_TIMEZONE = pytz.timezone('America/Los_Angeles')

ERRORS = []
ERROR_REPORT_PAGE = 'User:RheingoldRiver/GCD Errors'


async def main():
    # this has 2 entries in crontab, one for DST and one for not-DST
    # we only want this to run one time, so the first thing we do is make sure this is the DST-appropriate one
    if int(now_localized().strftime('%H')) != 23:
        return
    credentials = AuthCredentials(user_file="me")
    site = EsportsClient('lol', credentials=credentials)  # Set wiki
    pages = await get_pages_to_make()
    for k in pages.keys():
        # print(k)
        try:
            site.save_tile(k, text=pages[k], summary="Automatic GCD Backup")
            site.touch_title(k)
        except Exception as e:
            ERRORS.append(str(e))

    if len(ERRORS) > 0:
        site.save_tile(ERROR_REPORT_PAGE, text='<br>'.join(ERRORS))


async def get_pages_to_make():
    league_dict = await get_league_jsons()
    pages_to_create = {}
    for key in league_dict.keys():
        pages_to_create[archive_pattern(key)] = array_to_archive_table_str(league_dict[key])
        pages_to_create[current_pattern(key)] = array_to_current_table_str(league_dict[key])
    return pages_to_create


async def get_league_jsons():
    with open('gcd_leagues.txt') as f:
        leagues = f.readlines()
    leagues = [_.strip() for _ in leagues]
    to_jsonify = [i for i, league in enumerate(leagues) if league != 'SKIP']
    raw_jsons = await asyncio.gather(*[get_one_json(i) for i in to_jsonify])
    league_jsons = {}
    for response in raw_jsons:
        if response is not None:
            league_jsons[get_league_name(response)] = get_league_array(response)
    return league_jsons


async def get_one_json(i: int):
    try:
        return await get_one_json_retry(i)
    except JSONDecodeError:
        return None


def giveup_handler(details):
    ERRORS.append('Failed for region with index: ' + str(details['args'][0]))


def backoff_handler(details):
    print(details['tries'])


@backoff.on_exception(backoff.expo, JSONDecodeError, max_time=70,
                      on_backoff=backoff_handler,
                      on_giveup=giveup_handler)
async def get_one_json_retry(i: int):
    async with aiohttp.ClientSession() as session:
        url = GCD_URL.format(str(i + 2))
        async with session.get(url) as response:
            data = await response.read()
            return json.loads(data)


def get_league_name(response):
    return response['feed']['title']['$t']


def get_league_array(response):
    return entries_to_array(response['feed']['entry'])


def entries_to_array(entries):
    # entries is a 1-dimensional array of cells, 1-indexed
    # we are creating a 2-dimensional array of cells, 0-indexed
    array = []
    this_row = None
    num_rows_seen = 0
    for entry in entries:
        if entry_row(entry) > num_rows_seen:
            num_rows_seen = entry_row(entry)
            this_row = []
            array.append(this_row)
        while len(this_row) < entry_col(entry) - 1:
            this_row.append('')
        this_row.append(entry_text(entry))
    return array


def entry_row(entry):
    return int(entry['gs$cell']['row'])


def entry_col(entry):
    return int(entry['gs$cell']['col'])


def entry_text(entry):
    return entry['gs$cell']['$t']


def archive_pattern(key):
    return 'Archive:Global Contract Database/{}/{}'.format(key, get_now())


def current_pattern(key):
    return 'Archive:Global Contract Database/{}/Current'.format(key)


def get_now():
    return now_localized().strftime('%Y-%m-%d')


def now_localized():
    return datetime.datetime.now().astimezone(GCD_TIMEZONE)


def array_to_archive_table_str(wikitable):
    return ARCHIVE_INTRO.format(
        now_localized().strftime('%Y-%m-%d'),
        now_localized().strftime('%H:%M'),
        '{{subst:CURRENTYEAR}}-{{subst:CURRENTMONTH}}-{{subst:CURRENTDAY}}',
        '{{subst:CURRENTTIME}}'
    ) + array_to_table_str(wikitable) + '\n|}'


def array_to_current_table_str(wikitable):
    return CURRENT_INTRO + array_to_table_str(wikitable) + '\n|}'


def array_to_table_str(league_json):
    wikitable = ['{|']
    for i, row in enumerate(league_json):
        if i == 0:
            continue
        wikitable.append('|-')
        if i == 1:
            wikitable.append(json_row_to_title(row))
            continue
        wikitable.append(json_row_to_row(row))
    return '\n'.join(wikitable)


def json_row_to_title(row):
    # add 2 empty spaces at the end for parity with original C# version
    return '! ' + ' !! '.join(row) + ' '


def json_row_to_row(row):
    return '| ' + ' || '.join(row) + ' '


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
