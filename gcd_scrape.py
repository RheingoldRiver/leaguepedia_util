import datetime
import pytz
import requests
import time
from mwcleric.auth_credentials import AuthCredentials
from mwrogue.esports_client import EsportsClient

GCD_URL = "https://spreadsheets.google.com/feeds/cells/1Y7k5kQ2AegbuyiGwEPsa62e883FYVtHqr6UVut9RC4o/{}/public/values?alt=json"

ARCHIVE_INTRO = '<noinclude>{{{{GCDBackup|lastupdateddate={}|lastupdatedtime={}|pagecreationdate={}|pagecreationtime={}}}}}</noinclude>\n'

CURRENT_INTRO = '<noinclude>{{GCDBackupCurrent}}</noinclude>\n'

GCD_TIMEZONE = pytz.timezone('America/Los_Angeles')

ERRORS = []
ERROR_REPORT_PAGE = 'User:RheingoldRiver/GCD Errors'

def main():
	if int(now_localized().strftime('%H')) != 23:
		return
	credentials = AuthCredentials(user_file="me")
	site = EsportsClient('lol', credentials=credentials)  # Set wiki
	pages = get_pages_to_make()
	for k in pages.keys():
		# print(k)
		try:
			site.save_tile(k, text=pages[k], summary="Automatic GCD Backup")
			site.touch_title(k)
		except Exception as e:
			ERRORS.append(str(e))
	
	if len(ERRORS) > 0:
		# for sure wait out any rate limiting
		time.sleep(30)
		site.save_tile(ERROR_REPORT_PAGE, text='<br>'.join(ERRORS))

def get_pages_to_make():
	league_dict = get_league_jsons()
	pages_to_create = {}
	for key in league_dict.keys():
		pages_to_create[archive_pattern(key)] = array_to_archive_table_str(league_dict[key])
		pages_to_create[current_pattern(key)] = array_to_current_table_str(league_dict[key])
	return pages_to_create

def get_league_jsons():
	with open('gcd_leagues.txt') as f:
		leagues = f.readlines()
	leagues = [_.strip() for _ in leagues]
	league_jsons = {}
	for i, league in enumerate(leagues):
		if league != 'SKIP':
			# i is 0-indexed key in leagues
			# sheets is 1-indexed and the 1st one is just an info tab
			try:
				response = requests.get(GCD_URL.format(str(i + 2))).json()
			except Exception as e:
				time.sleep(30)
				try:
					response = requests.get(GCD_URL.format(str(i + 2))).json()
				except Exception as e:
					ERRORS.append(str(e))
					continue
			league_jsons[get_league_name(response)] = get_league_array(response)
	return league_jsons

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
	main()
