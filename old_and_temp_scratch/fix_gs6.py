import mwclient, mwparserfromhell, dateutil.parser, datetime
from log_into_wiki import *
limit = -1
templates = ["GameSchedule6","GameScheduleTST"]

thispage = site.pages["Template:GameScheduleTST"]

pages = thispage.embeddedin()

i = 0
for page in pages:
	if i == limit:
		break
	i = i + 1
	print(page.name)
	text = page.text()
	wikitext = mwparserfromhell.parse(text)
	for template in wikitext.filter_templates():
		if template.name.strip() in templates:
			if template.get("timezone").value.strip() == "TST":
				date = template.get("date").value.strip()
				time = template.get("time").value.strip()
				date_time = dateutil.parser.parse(date + " " + time)
				newtime = date_time + datetime.timedelta(hours=1)
				newtimetext = newtime.strftime("%H:%M")
				newdatetext = newtime.strftime("%Y-%m-%d")
				template.add("date",newdatetext)
				template.add("time",newtimetext)
				template.add("timezone", "KST")
			template.name = "GameSchedule5"
	newtext = str(wikitext)
	if newtext != text:
		page.save(newtext, summary="Updating GSTST/GS6 to GS5")