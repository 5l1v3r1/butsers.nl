from butsers.filestuff import filebasic


def getContent(userObject, parameters, configDict, databaseHandler):

	logContent = filebasic.getFileContent(configDict['staticDir'] + '/log/butsers.log.txt')

	return logContent, "text/html"