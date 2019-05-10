from log_into_wiki import *
import mwparserfromhell

site = login('me', 'lol')  # Set wiki
summary = 'Rearranging timeline params'  # Set summary

timeline_list = [
	"DynamicWeekTimeline6",
	"DynamicWeekTimeline7",
	"DynamicWeekTimeline8",
	"DynamicWeekTimeline8SLO",
	"TimelineT10W12 Lv2",
	"TimelineT10W9",
	"TimelineT4W2",
	"TimelineT6W5",
	"TimelineT6W5 v2",
	"TimelineT8W6",
	"TimelineT8W7",
	"TimelineT8W8",
	"TimelineT8W9",
	"TimelineT9W4",
	'TimelineOld'
]
all_pages = []
limit = -1
# startat_page = 'asdf'
for timeline in timeline_list:
	this_template = site.pages['Template:' + timeline]  # Set template
	pages = this_template.embeddedin()
	pages_var = list(pages)
	for page in pages_var:
		all_pages.append(page)
try:
	startat = pages_array.index(startat_page)
except NameError as e:
	startat = -1
except ValueError as e:
	startat = -1
print(startat)

lmt = 0
for page in all_pages:
	if lmt == limit:
		break
	lmt += 1
	if lmt < startat:
		print("Skipping page %s" % page.name)
	else:
		text = page.text()
		wikitext = mwparserfromhell.parse(text)
		for template in wikitext.filter_templates():
			if [_ for _ in timeline_list if template.name.matches(_)]:
				bg_list = []
				for param in template.params:
					if 'bg' in param.name:
						bg_list.append(param)
				for param in bg_list:
						template.remove(param.name)
						template.add(param.name,param.value)
		newtext = str(wikitext)
		if text != newtext:
			print('Saving page %s...' % page.name)
			page.save(newtext, summary=summary)
		else:
			print('Skipping page %s...' % page.name)