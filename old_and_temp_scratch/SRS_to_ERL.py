import mwparserfromhell, mwclient
from log_into_wiki import *

limit = -1

thispage = site.pages["Template:SeasonRosterSlot"]
pages = thispage.embeddedin(namespace=0)

i = 0
for page in pages:
	if i == limit:
		break
	i+=1
	print(page.name)
	text = page.text()
	wikitext = mwparserfromhell.parse(text)
	for template in wikitext.filter_templates():
		if template.name.matches("SeasonRosterStart"):
			template.name = "ExtendedRosterStart"
			if template.has("weeks"):
				template.add("rounds",template.get("weeks").value.strip())
				template.remove("weeks")
		elif template.name.matches("SeasonRosterEnd"):
			template.name = "ExtendedRosterEnd"
		elif template.name.matches("SeasonRosterSlot"):
			template.name = "ExtendedRosterLine"
			names = template.get("player").value.split("{{!}}")
			if len(names) == 2:
				template.add("player",names[1])
				template.add("link",names[0],before="name")
			j = 1
			jstr = "week" + str(j)
			weeks = []
			while template.has(jstr):
				w = template.get(jstr).value.strip()
				if w == "":
					weeks.append("n")
				else:
					weeks.append(w[0])
				template.add("r",", ".join(weeks))
				template.remove(jstr)
				j+=1
				jstr = "week" + str(j)
	newtext = str(wikitext)
	if newtext != text:
		print("Saving...")
		page.save(newtext,summary="Automatically updating SRS to ERL",tags="SRS_to_ERL")
	else:
		print("No change, skipping page")