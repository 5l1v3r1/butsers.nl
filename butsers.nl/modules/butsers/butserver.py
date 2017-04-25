
import importlib
from butsers.sanitation import sanitize
from butsers.filestuff import filebasic
from butsers.debugging import debugbasic


class Butserver(object):
	""" Server class for butsers.nl """

	def __init__(self, configDict, databaseHandler):
		self.configDict = configDict
		self.databaseHandler = databaseHandler


	def serveContent(self, content, contentType="text/plain"):
		''' Serve some content to the user '''

		print "Content-Type:" + contentType + ";charset=utf-8"
		print ""
		print content.encode('utf8')


	def tryLogin(self, parameters):
		pass


	def getUserObject(self):
		return {}


	def handleRequest(self, queryString, parameters):
		''' Handle requests for butsers.nl '''

		if len(parameters.keys()) == 0:
			requestedModule = 'index'
		else:
			requestedModule = parameters.getfirst("mod", "").lower()

		if sanitize.isSaneData(requestedModule):
			
			if requestedModule == 'login':
				self.tryLogin(parameters)
				return

			else:
				for moduleName in self.configDict['modulesEnabled'] + ['index']: # index is a special purpose page
					if moduleName == requestedModule:
						pageModule = importlib.import_module('..module'+moduleName, 'butsers.subpkg') 

						userObject = self.getUserObject()

						content, contentType = pageModule.getContent(userObject, parameters, self.configDict, self.databaseHandler)
						self.serveContent(content, contentType)
						return

		self.serveContent("wat", "text/html")


