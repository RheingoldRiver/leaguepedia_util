from river_mwclient.esports_site import EsportsSite
import time
limit = -1
site = EsportsSite('lol', user_file="me") # Set wiki
t = site.client.pages["Template:TeamRoster"]

pages = t.embeddedin()

c = site.client.categories['Pages with script errors']

pages = t.embeddedin()

startat_page = None
passed_startat = True

lmt = 0
#for p in c:
for p in pages:
	if lmt == limit:
		break
	if p.name == startat_page:
		passed_startat = True
	if not passed_startat:
		continue
	lmt += 1
	print(p.name)
	text = p.text()
	try:
		p.save(text,'blank editing')
	except Exception as e:
		print('uh oh!!!!!!!!')
		time.sleep(10)
		p.save(text, 'blank editing')
