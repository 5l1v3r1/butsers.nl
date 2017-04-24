
import importlib
from sanitation import sanitize

from butsers.filestuff import filebasic


class Butserver(object):
	""" Server class for butsers.nl """

	def __init__(self, configDict, databaseHandler):
		self.configDict = configDict
		self.modules = self.configDict['modulesEnabled']
		self.staticDir = self.configDict['staticDir']
		self.databaseHandler = databaseHandler

	def serveContent(self, content, contentType="text/plain"):
		''' Serve some content to the user '''

		print "Content-Type:" + contentType + ";charset=utf-8"
		print ""
		print content.encode('utf8')

	def showIndexPage(self):
		''' Show the main page '''

		indexPageJS = filebasic.getFileContent(self.staticDir + '/index/index.js')
		indexPageJS = indexPageJS.replace('{NAVPAGESPACE}', '"'+'","'.join(self.modules)+'"')

		indexPageCSS = filebasic.getFileContent(self.staticDir + '/index/index.css')

		indexPageTemplate = filebasic.getFileContent(self.staticDir + '/index/index.template')
		indexPageTemplate = indexPageTemplate.replace('{STYLESPACE}', indexPageCSS)
		indexPageTemplate = indexPageTemplate.replace('{SCRIPTSPACE}', indexPageJS)

		self.serveContent(indexPageTemplate, "text/html")


	def tryLogin(self, parameters):
		pass

	def getUserObject(self):
		return {}

	def handleRequest(self, queryString, parameters):
		''' Handle requests for butsers.nl '''

		if len(parameters.keys()) == 0:
			self.showIndexPage()

		else:
			requestedModule = parameters.getfirst("mod", "").lower()
			if sanitize.isSaneData(requestedModule):
				
				if requestedModule == 'login':
					self.tryLogin(parameters)
					return

				else:
					for moduleName in self.modules:
						if moduleName == requestedModule:
							pageModule = importlib.import_module('..module'+moduleName, 'butsers.subpkg') 

							userObject = self.getUserObject()

							content, contentType = pageModule.getContent(userObject, parameters, self.configDict, self.databaseHandler)
							self.serveContent(content, contentType)
							return

			self.serveContent("wat", "text/html")