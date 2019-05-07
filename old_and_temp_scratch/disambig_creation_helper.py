import re, threading, mwclient, mwparserfromhell
from disambig_creation_constants import *
from log_into_wiki import *

def savepage(targetpage,savetext):
	targetpage.save(savetext, summary=summary, tags="bot_disambig")

def blank_edit_page(page):
	textname = str(page.name)
	newpage = site.pages[textname]
	text = newpage.text(cache=False)
	page.save(text,summary="Blank Editing")

def movepage(fromPage):
	newPageName = str(fromPage.name).replace(originalName, newName)
	newPage = site.pages[newPageName]
	if newPage.exists:
		print("{} already exists, cannot move!".format(fromPage.name))
	else:
		print("Moving page {} to {}".format(fromPage.name, newPageName))
		fromPage.move(newPageName, reason=summary, no_redirect=True)
		blankEditThese.append(newPage)

def editconcept(concept):
	text = concept.text()
	wikitext = mwparserfromhell.parse(text)
	for template in wikitext.filter_templates():
		if template.name.matches("PlayerGamesConcept"):
			i = 1
			while template.has(i):
				if template.get(i).strip() == originalName:
					template.add(i,newName)
				elif template.get(i).strip() == origNameLC:
					template.add(i,newNameLC)
				i = i + 1
	newtext = str(wikitext)
	if newtext != text:
		concept.save(newtext, summary=summary, tags="bot_disambig")

def save_css_page():
	csspage = site.pages["MediaWiki:Gadget-highlightDisambigs.css"]
	csstext = csspage.text()
	if originalName not in csstext:
		# use re in case a human edited the page and didn't use exactly the expected styling
		# remove the style from the string
		s = csstext.split('{')[0]
		# split string to capture the page titles
		tbl = re.split('a\\[title="\s*(.+?)\s*\"\\],?\s*',s)
		tbl.append(originalName)
		tblSorted = sorted(tbl)
		# re-add style
		tblSorted2 = ['a[title="{}"]'.format(s) for s in tblSorted if s.strip(", ") != ""]
		# concatenage back into a string
		csstext = ', '.join(tblSorted2) + cssStyle
		print("Saving css page...")
		csspage.save(csstext, summary=summary, tags="bot_disambig")

def editsubpage(subpage):
	text = subpage.text()
	wikitext = mwparserfromhell.parse(text)
	for stemplate in wikitext.filter_templates():
		if stemplate.has(1):
			if stemplate.get(1).value.strip() == originalName:
				stemplate.add(1, newName)
	newtext = str(wikitext)
	if text != newtext:
		print("Editing " + subpage.name + "...")
		subpage.save(newtext, reason=summary)

def processpage(page):
	print("Processing next page: " + page.name)
	text = page.text()
	origtext = text
	# do links first because it's easier to just edit them as a string
	text = text.replace("[[" + originalName + "]]", "[[" + newName + "|" + originalName + "]]")
	wikitext = mwparserfromhell.parse(text)
	for template in wikitext.filter_templates():
		processtemplate(template)
	newtext = str(wikitext)
	if origtext != newtext or blankedit:
		print("Saving...")
		t = threading.Thread(target=savepage, kwargs={"targetpage": page, "savetext": newtext})
		t.start()
		t.join(timeout=timeoutLimit)
	else:
		print("No changes, skipping")

def processtemplate(template):
	if template.name.matches('bl') and template.get(1).value.strip() == originalName and not template.has(2):
		template.add(1, newName)
		template.add(2, originalName)
	
	elif template.name.strip() in listplayerTemplates and template.get(
					1).value.strip() == originalName and not template.has("link"):
		template.add("link", newName, before=1)
	
	elif template.name.strip() in rosterTemplates \
					and template.get("player").value.strip() == originalName \
					and not template.has("link"):
		template.add("link", newName, before="name")
	
	elif template.name.matches('TeamRoster'):
		j = 1
		jstr = str(j)
		while template.has("player" + jstr):
			if template.get("player" + jstr).value.strip() == originalName and not template.has("link" + jstr):
				template.add("link" + jstr, newName, before="flag" + jstr)
			j = j + 1
			jstr = str(j)
	
	elif template.name.strip() in scoreboardTemplates and template.get("name").value.strip() == originalName:
		template.add("link", newName, before="kills")
	
	elif template.name.strip() in rosterChangeTemplates and template.get("player").value.strip() == originalName:
		template.add("player", newName + "{{!}}" + originalName)
	
	elif template.name.matches("LCSPlayerLine") and template.get(1).strip() == originalName:
		template.add(2, newName)
	
	elif template.name.matches("Player") and template.get(1).strip() == originalName:
		template.add('link', newName)
	
	elif template.name.matches("RSCR/Line"):
		if template.has("p1"):
			if template.get("p1").strip() == originalName:
				template.add("p1", newName + "{{!}}" + originalName)
		if template.has("p2"):
			if template.get("p2").strip() == originalName:
				template.add("p2", newName + "{{!}}" + originalName)

def make_disambig_page():
	text = "{{DisambigPage\n|player1=" + newName + "\n|player2=\n}}"
	page = site.pages[originalName]
	page.save(text,summary=summary)