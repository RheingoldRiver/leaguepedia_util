from log_into_wiki import *
import mwparserfromhell

site = login('bot', 'lol')  # Set wiki
summary = 'Forcing blank edit'  # Set summary

limit = -1
startat_page = 'Faaa'
this_template = site.pages['Template:Infobox Player']  # Set template
pages = this_template.embeddedin()

pages_var = list(pages)

pages_array = [p.name for p in pages_var]

try:
	startat = pages_array.index(startat_page)
except NameError as e:
	startat = -1
except ValueError as e:
	startat = -1
print(startat)

n = 50
slices = [pages_array[i:i+n] for i in range(0,len(pages_array), n)]

lmt = 0
for s in slices:
	print(s[0])
	pagelist = '|'.join(s)
	site.api('purge', format='json',
			 titles = pagelist,
			 forcelinkupdate = '1'
			 )