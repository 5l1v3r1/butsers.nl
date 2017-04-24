from butsers.debugging import debugbasic
from butsers.filestuff import filebasic
import datetime



def sanitizeNieuwsValue(val):
	return val.replace('"','')



def getContent(userObject, parameters, configDict, databaseHandler):

	staticDir = configDict['staticDir']

	newsEntries = databaseHandler.selectLatest("nieuws_entries", "linkPublished", maxResults = 50, sortOrder='DESC')

	nieuwsPageTemplate = filebasic.getFileContent(staticDir + '/nieuws/nieuws.template')
	nieuwsPageCSS = filebasic.getFileContent(staticDir + '/nieuws/nieuws.css')

	nieuwsPageTemplate = nieuwsPageTemplate.replace('{STYLESPACE}', nieuwsPageCSS)

	nieuwsEntryTemplate = filebasic.getFileContent(staticDir + '/nieuws/nieuws.entry.template')

	allEntries = ""
	allSources = ""
	sourceDict = {}

	sourceTemplate = filebasic.getFileContent(staticDir + '/nieuws/nieuws.source.template')

	sourceEntries = databaseHandler.selectAll("nieuws_sources")
	for sourceEntry in sourceEntries:
		sourceId, sourceName, sourceURL, sourceB64Image = sourceEntry
		sourceDict[sourceId] = (sourceName, sourceURL, sourceB64Image)

		sourceName = sanitizeNieuwsValue(sourceName)
		sourceB64Image = sanitizeNieuwsValue(sourceB64Image)
		sourceURL = sanitizeNieuwsValue(sourceURL)

		newEntry = sourceTemplate.replace("{IMGALT}", sourceName)
		newEntry = newEntry.replace("{IMAGEB64}", sourceB64Image)
		newEntry = newEntry.replace("{SOURCELINK}", sourceURL)
		newEntry = newEntry.replace("{SOURCEDESC}", sourceName)

		allSources += newEntry + "\n"

	nieuwsPageTemplate = nieuwsPageTemplate.replace('{SOURCESPACE}', allSources)


	for entry in newsEntries:
		entryId, sourceId, linkURL, linkDesc, linkPublished = entry

		sourceName, sourceURL, sourceB64Image = sourceDict[sourceId]

		# remove double quotes
		sourceName = sanitizeNieuwsValue(sourceName)
		sourceB64Image = sanitizeNieuwsValue(sourceB64Image)
		linkURL = sanitizeNieuwsValue(linkURL)
		linkDesc = sanitizeNieuwsValue(linkDesc)

		# fix weird urls
		if linkURL[:4] != 'http':
			linkURL = 'https://' + linkURL

		# final fixes
		if len(linkDesc) > 83:
			linkDesc = linkDesc[:83] + "..."

		newEntry = nieuwsEntryTemplate.replace('{IMGALT}', sourceName)
		newEntry = newEntry.replace('{IMAGEB64}', sourceB64Image)
		newEntry = newEntry.replace('{LINKURL}', linkURL)
		newEntry = newEntry.replace('{LINKDESC}', linkDesc)

		st = datetime.datetime.fromtimestamp(linkPublished).strftime('%Y-%m-%d %H:%M:%S')
		newEntry = newEntry.replace('{LINKPUB}', str(st))

		allEntries += "\n" + newEntry

	nieuwsPageTemplate = nieuwsPageTemplate.replace('{TABLESPACE}', allEntries)
	
	return nieuwsPageTemplate, "text/html"

