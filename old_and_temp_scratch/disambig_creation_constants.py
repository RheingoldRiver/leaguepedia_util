originalName = 'Limit'
irlName = 'Ju Min-gyu'
newName = '{} ({})'.format(originalName,irlName)
initmove = True
blankedit = False
limit = -1
timeoutLimit = 30

listplayerTemplates = ["listplayer", "listplayer/Current"]
rosterTemplates = ["ExtendedRosterLine", "ExtendedRosterLine/MultipleRoles"]
scoreboardTemplates = ["MatchRecap/Player", "MatchRecapS4/Player",
					   "MatchRecapS5/Player", "MatchRecapS6/Player",
					   "MatchRecapS7/Player", "MatchRecapS8/Player",
					   "MatchRecapS6NoSMW/Player", "MatchRecapS7NoKeystones/Player"]
statTemplates = ["IPS","CareerPlayerStats","MatchHistoryPlayer"]
rosterChangeTemplates = ["RosterChangeLine","RosterRumorLine2"]
summary = "Disambiguating {} to {}".format(originalName, newName)

cssStyle = "{\n    color:orange!important;\n    font-weight:bold;\n}"

origNameLC = originalName[0].lower() + originalName[1:]
newNameLC = newName[0].lower() + newName[1:]

blankEditThese = []