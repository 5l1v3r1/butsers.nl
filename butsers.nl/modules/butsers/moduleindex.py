from butsers.filestuff import filebasic


def getContent(userObject, parameters, configDict, databaseHandler):
	''' Show the index page '''

	staticDir = configDict['staticDir']

	indexPageJS = filebasic.getFileContent(staticDir + '/index/index.js')
	indexPageJS = indexPageJS.replace('{NAVPAGESPACE}', '"'+'","'.join(configDict['modulesEnabled'])+'"')

	indexPageCSS = filebasic.getFileContent(staticDir + '/index/index.css')

	indexPageTemplate = filebasic.getFileContent(staticDir + '/index/index.template')
	indexPageTemplate = indexPageTemplate.replace('{STYLESPACE}', indexPageCSS)
	indexPageTemplate = indexPageTemplate.replace('{SCRIPTSPACE}', indexPageJS)

	return indexPageTemplate, "text/html"
