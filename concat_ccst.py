import mwclient

from log_into_wiki import *

result = site.api("query",
					   list = "categorymembers",
					   cmtitle = "Category:Sister Team Cargo Concepts",
					   cmlimit = "max",
					   cmprop = 'title'
					   )

cat_tbl = []

for page in result['query']['categorymembers']:
	cat_tbl.append(page['title'])

cat_str = "|".join(cat_tbl)

result = site.api("query",
				 prop = "revisions",
				 titles = cat_str,
				 rvprop = "content"
				 )

content_tbl = []

for page in result['query']['pages'].values():
	content_tbl.append(page["revisions"][0]["*"])

text = '\n'.join(content_tbl)

page = site.pages["CargoConcept:SisterTeams"]

page.save(text,summary="Concatenating Sister Teams Cargo Concepts")