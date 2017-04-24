from butsers.debugging import debugbasic
import sqlite3

class ButsDB(object):
	"""docstring for ButsDB"""

	def __init__(self, configDict):
		self.configDict = configDict
		self.dbFile = configDict['dbFile']
		self.conn = None
		self.c = None

	def init(self):
		self.conn = sqlite3.connect(self.dbFile)
		self.c = self.conn.cursor()

	def close(self):
		self.conn.commit()
		self.conn.close()

	def selectLatest(self, table, columnName, maxResults = 10, sortOrder = 'ASC'):

		# No safe table stuff in sqlite3 :'(
		# TODO: in-depth sec
		query = "SELECT * from " + table + " ORDER BY " + columnName + " " + sortOrder + " LIMIT " + str(maxResults)
		
		self.c.execute(query)
		entries = self.c.fetchall()
		return entries

	def selectSingle(self, table, whereColumn, whereValue):

		# No safe table stuff in sqlite3 :'(
		# TODO: in-depth sec
		query = "SELECT * from " + table + " WHERE " + whereColumn + " = ? LIMIT 1"

		self.c.execute(query, (whereValue,))
		entry = self.c.fetchone()
		return entry



	def selectAll(self, table):

		# No safe table stuff in sqlite3 :'(
		# TODO: in-depth sec
		query = "SELECT * from " + table

		self.c.execute(query)
		entries = self.c.fetchall()
		return entries