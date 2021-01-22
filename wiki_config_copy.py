import time
from collections import OrderedDict

from river_mwclient.wiki_client import WikiClient
from river_mwclient.auth_credentials import AuthCredentials

credentials = AuthCredentials(user_file="wc")
site = WikiClient('pcj-testing-ucp.fandom.com', credentials=credentials)

FROM_WIKI_ID = 2293615
FROM_WIKI_NAME = 'Leaguepedia'
TO_WIKI_ID = 2415957

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
	if param in SKIP_PARAMS or param in ALREADY_PARAMS:
		continue
	if param.endswith('Ext') and 'Enable' in param:
		continue
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