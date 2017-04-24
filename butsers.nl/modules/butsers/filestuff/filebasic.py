
def getFileContent(fileName):
	''' Return the content of some file '''

	with open(fileName) as fin:
		return fin.read()

