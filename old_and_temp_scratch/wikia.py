from river_mwclient.esports_site import EsportsSite

site = log_into_fandom('me', 'leagueoflegends')

print(site.client.pages['Sona'].text())

