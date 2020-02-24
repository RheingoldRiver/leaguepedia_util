from river_mwclient.esports_site import EsportsSite
import mwparserfromhell
summary = 'auto updating residency to PCS'
with open('pages.txt', encoding='utf-8') as f:
	titles = f.readlines()

titles = [_.strip() for _ in titles]

site = EsportsSite('lol', user_file="me") # Set wiki

result = site.client.api(action="query", list="querypage", qppage="DoubleRedirects")
for item in result['query']['querypage']['results']:
	source_page = site.client.pages[item['title']]
	target_title = item['databaseResult']['c_title']
	target_namespace_number = int(item['databaseResult']['c_namespace'])
	target_namespace = site.client.namespaces[int(target_namespace_number)]
	target_page_name = '{}{}'.format(
		target_namespace + ':' if target_namespace != '' else '',
		target_title
	)
	source_page.save('#redirect[[%s]]' % target_page_name, summary="bot edit!!!!!!!")
