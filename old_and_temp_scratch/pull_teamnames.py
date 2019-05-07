from log_into_wiki import *
site = login('me','rl-esports')

suffixes = ['1','2','3','4','5','6','7','8','9','0','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
text = []
for suffix in suffixes:
	p = 'Template:TeamImage/' + suffix
	page = site.pages[p]
	text.append(page.text())

with open('rl teamimage.txt','w', encoding="utf-8") as f:
	f.write('\n'.join(text))