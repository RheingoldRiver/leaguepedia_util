from esports_site import EsportsSite
import mwparserfromhell

site = EsportsSite('bot', 'lol')

for page in site.categories['Champions']:
    text = page.text()
    wikitext = mwparserfromhell.parse(text)
    title = None
    for t in wikitext.filter_templates():
        if t.name.matches('Infobox Champion'):
            title = t.get('title').value.strip()
    new_page = '{} - {}'.format(page.name, title)
    new_text = '#redirect[[%s]]' % page.name
    site.pages[new_page].save(new_text)
    new_mh_page = new_page + '/Match History'
    site.pages[new_mh_page].save('#redirect[[%s/Match History]]' % page.name)
