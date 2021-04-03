import time
from collections import OrderedDict

from mwcleric.wiki_client import WikiClient
from mwcleric.auth_credentials import AuthCredentials

credentials = AuthCredentials(user_file="wc")
site = WikiClient('https://pcj.fandom.com', credentials=credentials)

wiki_name_to_id_map = {
	"apexlegends-esports": 2294647,
	"cod-esports": 2294030,
	# "commons-esports": 2342996,
	"default-loadout-esports": 2293768,
	"help-esports": 2293305,
	"fifa-esports": 2294151,
	# "fortnite-esports": 2294263,
	"gears-esports": 2293557,
	"halo-esports": 2294143,
	"legendsofruneterra-esports": 2295319,
	"lol": 2293615,
	"nba2k-esports": 2293897,
	"paladins-esports": 2293440,
	"pubg-esports": 2293890,
	"rl-esports": 2294760,
	"rollerchampions-esports": 2536304,
	"siege-esports": 2294358,
	"smite-esports": 2293467,
	"splatoon2-esports": 2295280,
	"teamfighttactics": 2295108,
	"valorant-esports": 2295329,
	"vg-esports": 2294444,
	"wildrift-esports": 2415957,
}

FROM_WIKI_ID = 2293615
FROM_WIKI_NAME = 'Leaguepedia'
TO_WIKI_ID = 2295319

SKIP_PARAMS = ['wgSitename', 'wgMetaNamespace', 'wgUploadPath', 'wgUploadDirectory', 'wgLogo',
               'wgLocalInterwiki', 'wgCacheEpoch', 'wgDartCustomKeyValues',
               'wgWikiDirectedAtChildrenByFounder', 'wgWikiDescription', 'wgEnableHydraFeatures',
               'wgDefaultSkin', 'wgActorTableSchemaMigrationStage', 'wgUCPMigrationDone',
               'wgUCPMigrationDate', 'wgAdDriverPagesWithoutAds', 'wgEnableAudioButton', 'wgWidgetsCompileDir',
               'dsSiteKey']
ALREADY_PARAMS = ['wgEnableUserEmail', 'wgLanguageCode', 'wgRestrictionLevels']
OKAY_PARAMS = ['wgEnableUserEmail', 'wgRestrictionLevels', 'wgNamespacesToBeSearchedDefault',
               'wgExtraNamespacesLocal', 'wgRightsText', 'wgRightsIcon', 'wgContentNamespaces',
               'wgGroupPermissionsLocal', 'wgWikiaEnableDPLExt', 'wgEnableGadgetsExt',
               'wgEnableLoopsExt', 'wgAddGroupsLocal', 'wgRemoveGroupsLocal', 'wgRestrictDisplayTitle',
               'wgEnableAbuseFilterExtension', 'wgEnableArrayExt', 'wgCargoPageDataColumns',
               'wgClaimWikiEnabled', 'wgCustomLogsLogs', 'wgFlaggedRevsNamespaces',
               'wgFlaggedRevsHandleIncludes', 'wgFlaggedRevsAutopromote', 'wgHighlightLinksInCategory',
               'wgCascadingRestrictionLevels', 'wgRegexFunctionsPerPage', 'wgtoNamespacesWithTooltips',
               'wgtoEnableInNamespaces', 'wgVisualEditorDisableForAnons', 'wgSkipSkins', 'wgUseEsportsCommons',
               'wgGrantPermissionsLocal'
               ]

with open('wc_params_copy.txt') as f:
	params = f.readlines()

for param in params:
	param = param.strip()
	if param not in OKAY_PARAMS:
		continue
	print('Starting param ', param)
	token=site.client.get_token('csrf')
	result = site.client.api('variableinfo', wiki_id=str(FROM_WIKI_ID), variable_name=param,
	                      token=token)
	val = result['variable_details']['value']
	if val is not None:
		if type(val) == list:
			val = '[' + ', '.join(['"{}"'.format(_) for _ in val]) + ']'
		elif type(val) == OrderedDict:
			t = []
			for k, v in val.items():
				if type(v) == str:
					t.append('  "{}": "{}"'.format(k, v))
					
				# wgGrantPermissionsLocal has nested ordered dicts
				elif type(v) == OrderedDict:
					t2 = []
					for k2, v2 in v.items():
						t2.append('    "{}": "{}"'.format(k2, v2))
					# k, v is the outer ordered dict key/value pair
					t.append('  ' + '"{}": '.format(k) + '{\n' + ',\n'.join(t2) + '\n  }')
			val = '{\n' + ',\n'.join(t) + '\n}'
		print('Setting {} to {}'.format(param, val))
		if param not in OKAY_PARAMS:
			time.sleep(10)
		site.client.api('savewikiconfigvariable', wiki_id=str(TO_WIKI_ID), variable_name=param,
	                variable_value=val, reason="Cloning value from {}".format(FROM_WIKI_NAME),
	                token=token)