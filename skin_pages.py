from river_mwclient.esports_site import EsportsSite

site = EsportsSite('lol', user_file="me") # Set wiki
summary = 'Populate skin pages' # Set summary

pages = site.cargo_client.page_list(tables="SkinImages,_pageData=PD",join_on="SkinImages.Name=PD._pageName",fields="Name",where="Name IS NOT NULL and PD._pageName IS NULL")

for p in pages:
	if not p.exists:
		p.save('{{Champion Skins Navbox}}\n{{Infobox Skin}}\n{{ChampionSkinIntro}}\n{{ChampionSkinImageSections}}')
