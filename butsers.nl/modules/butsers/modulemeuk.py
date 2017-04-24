from butsers.filestuff import filebasic



def getContent(userObject, parameters, configDict, databaseHandler):

	meukTemplate = filebasic.getFileContent(configDict['staticDir'] + '/meuk/meuk.template')
	
	return meukTemplate, "text/html"


