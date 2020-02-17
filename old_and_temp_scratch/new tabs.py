from log_into_wiki import *
import mwparserfromhell
import mwclient.page as Page

site = login('bot', 'lol')
summary = 'using new tabs ns'

tab:Page
for tab in site.categories['Tournament Tabs']:
    if tab.namespace == 10018:
        print('{} already moved'.format(tab.name))
        continue
    new_name = 'Tabs:{}'.format(tab.page_title.replace(' Tabs', ''))
    tab.move(new_name, reason=summary)
    for page in tab.embeddedin():
        text = page.text()
        wikitext = mwparserfromhell.parse(text)
        for template in wikitext.filter_templates():
            if tl_matches(template, [tab.page_title]):
                template.name = new_name

        newtext = str(wikitext)
        if text != newtext:
            print('Saving page %s...' % page.name)
            page.save(newtext, summary=summary)
        else:
            print('Skipping page %s...' % page.name)
    tab.delete(reason=summary)
