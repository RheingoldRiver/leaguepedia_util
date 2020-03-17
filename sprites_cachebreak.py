from river_mwclient.esports_client import EsportsClient
from river_mwclient.auth_credentials import AuthCredentials
import re

credentials = AuthCredentials(user_file="me")
site = EsportsClient('lol', credentials=credentials) # Set wiki
summary = 'Bot Edit - Automatically Forcing Sprite Cache Update'
url_re_start = r'.*(\/.\/..\/)'
url_re_end = r'(\?version=\w*)\".*'
css_page_list = ['MediaWiki:Common.css', 'MediaWiki:Mobile.css']

category_result = site.client.api('query', list = 'categorymembers', cmtitle = 'Category:Sprite Images', cmlimit = 50)
file_name_list = [_['title'] for _ in category_result['query']['categorymembers']]

parse_text_list = ['[[%s|link=]]' % _ for _ in file_name_list]
parse_text = '!!!'.join(parse_text_list)
result = site.client.api('parse', text = parse_text, title = 'Main Page', disablelimitreport = 1)
text = result['parse']['text']['*']

css_texts_old = []
css_texts_new = []
for file_name in file_name_list:
	raw_name = file_name.replace('File:', '')
	re_full = url_re_start + re.escape(raw_name) + url_re_end
	match = re.match(re_full, text)
	css_texts_new.append(match[1] + raw_name + r'\1' + match[2])
	css_texts_old.append(re.escape(match[1] + raw_name) + r'(.*)' + r'\?version=\w*')
	
def replace_css_in_file(css_page):
	css_page_text = css_page.text()
	css_page_text_new = css_page_text
	for i, v in enumerate(css_texts_old):
		css_page_text_new = re.sub(v, css_texts_new[i], css_page_text_new)
	if css_page_text != css_page_text_new:
		css_page.save(css_page_text_new, summary = summary)

for page_name in css_page_list:
	replace_css_in_file(site.client.pages[page_name])

