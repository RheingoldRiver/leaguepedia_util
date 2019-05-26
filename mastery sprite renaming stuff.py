import re
from log_into_wiki import *

site = login('bot', 'lol')

with open('mastery sprite data.txt', encoding="utf-8") as f:
	lines = f.readlines()

t = []

for line in lines:
	t.append(line)
	logo = re.search(r'"(.+?)"', line)[1]
	pos = re.search(r'pos = ([0-9]*)', line)[1]
	page = site.pages['File:Mastery ' + logo + '.png']
	print(page.name)
	for p in page.backlinks(namespace=6,redirect=True):
		print('redirect - %s' % p.name)
		file_name = p.name.replace('.png', '').replace('File:Mastery ', '')
		t.append('\t\t["{}"] = {{ pos = {}, section = 1 }},'.format(file_name, pos))
	

with open('league sprite data new.txt', 'w', encoding='-utf8') as f:
	f.write('\n'.join(t))