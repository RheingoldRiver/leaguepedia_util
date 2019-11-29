from log_into_wiki import *
import mwparserfromhell, datetime
limit = -1

site = login('bot', 'fortnite-esports')
summary = 'Automatically setting active/inactive status'

def change_active_status(result, status):
    for p in result:
        text = p.text()
        wikitext = mwparserfromhell.parse(text)
        for tl in wikitext.filter_templates():
            if tl.name.matches('Infobox Player'):
                tl.add('isinactive', status)
        newtext = str(wikitext)
        if newtext != text:
            p.save(newtext, summary=summary)

now = datetime.datetime.now()
then = now - datetime.timedelta(days=6*28)

result = site.cargo_pagelist(
                  tables='Tournaments=T,TournamentResults=Res, TournamentResults__RosterLinks=RL,PlayerRedirects=PR,Players=P',
                  join_on = 'T._pageName=Res.OverviewPage,Res._ID=RL._rowID,RL._value=PR.AllName,PR._pageName=P._pageName',
                  where = 'P.IsInactive="1"',
                  fields = 'P._pageName=player',
                  having = 'COUNT(*)>1',
                  )

change_active_status(result, 'No')

result = site.cargo_pagelist(
                  tables='Tournaments=T,TournamentResults=Res, TournamentResults__RosterLinks=RL,PlayerRedirects=PR,Players=P',
                  join_on = 'T._pageName=Res.OverviewPage,Res._ID=RL._rowID,RL._value=PR.AllName,PR._pageName=P._pageName',
                  where = 'P.IsInactive IS NULL OR P.IsInactive="0"',
                  fields = 'P._pageName=player',
                  having = 'COUNT(*)=1 AND MAX(T.Date) <="{}"'.format(then.strftime('%Y-%m-%d')),
                  )

change_active_status(result, 'Yes')
