import re, urllib.request, io
from esports_site import EsportsSite
from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

def login(user, wiki, timeout = 30):
		return EsportsSite(user, wiki)

def log_into_fandom(user, wiki):
	if user == 'me':
		password = open('password_fandom.txt').read().strip()
		site = extended_site.ExtendedSite('%s.fandom.com' % wiki, path='/')
		site.login('RheingoldRiver', password)
		return site

def report_errors(report_page, page, errors):
	text = report_page.text()
	error_text = '\n* '.join([e.args[0] for e in errors])
	newtext = text + '\n==Python Error Report==\nPage: [[{}]] Messages:\n* {}'.format(page, error_text)
	report_page.save(newtext)

def api_parse_query(site, datatype, values):
	query_text = '{{#invoke:PrintParsedText|unordered|type=' + datatype + '|' + '|'.join(values) + '}}'
	query_result = site.api(
		'parse',
		format='json',
		text=query_text,
		prop='text',
		disablelimitreport=1,
		wrapoutputclass=''
	)
	result = query_result['parse']['text']['*']
	result = result.replace('<p>', '').replace('\n</p>', '')
	result_tbl = result.split(',')
	return result_tbl

def parse_ordered_field(val, sep):
	if not sep:
		sep = ','
	tbl = re.split('\s*' + sep + '\s*' + '\s*', val)
	return tbl

def check_links(template, key1, key2, sep, name, link):
	if not sep:
		sep = ','
	if template.has(key1):
		val1 = template.get(key1).value.strip()
		tbl1 = parse_ordered_field(val1, sep)
		tbl2 = ['' for _ in range(len(tbl1))] # list(range(len(tbl1)))
		if template.has(key2):
			val2 = template.get(key2).value.strip()
			tbl2 = parse_ordered_field(val2, sep)
		if name in tbl1:
			i = tbl1.index(name)
			tbl2[i] = link
			template.add(key2,sep.join(tbl2), before=key1)
			template.add(key1, val1, before=key2)

def get_filename_url_to_open(site, filename, size=None):
	pattern = r'.*src\=\"(.+?)\".*'
	size = '|' + str(size) + 'px' if size else ''
	to_parse_text = '[[File:{}|link=%s]]'.format(filename, size)
	result = site.api('parse', title='Main Page', text=to_parse_text, disablelimitreport=1)
	parse_result_text = result['parse']['text']['*']
	print(parse_result_text)
	url = re.match(pattern, parse_result_text)[1]
	return url

def open_file_url(url):
	return Image.open(io.BytesIO(urllib.request.urlopen(url).read()))

def open_image_from_filename(site, filename, size=None):
	url = get_filename_url_to_open(site, filename, size=size)
	return open_file_url(url)

def tl_matches(tl, arr):
	return [_ for _ in arr if tl.name.matches(_)]
