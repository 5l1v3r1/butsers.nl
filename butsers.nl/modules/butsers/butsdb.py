from butsers.debugging import debugbasic
from butsers.sanitation import sanitize

import sqlite3


class ButsDB(object):
	""" Database class for butsers.nl """

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


	def isSafeTableName(self, tableName):
		''' Check if table name is in proper format and exists '''
		
		if sanitize.isSaneData(tableName, allowedCharacters = "abcdefghijklmnopqrstuvwxyz-_", allowedLength = 31):
			self.c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?",(tableName,))
			if self.c.fetchone() != None:
				return True

		return False


	def isSafeColumnName(self, columnName):
		''' Check if column name is in proper format '''
		
		if sanitize.isSaneData(columnName, allowedLength = 31, allowedCharacters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"):
			return True

		return False


	def isSafeMaxResults(self, maxResults):
		''' Check if max results integer is in proper format '''
		
		try:
			i = int(maxResults)
			if i > 0 and i < 1327:
				return True
		except:
			return False
		return False


	def isSafeSortOrder(self, sortOrder):
		''' Check if sort order is in proper format '''

		return sortOrder == 'ASC' or sortOrder == 'DESC'


	def selectLatest(self, table, columnName, maxResults = 10, sortOrder = 'ASC'):
		''' Returns the latest x entries for a certain table/column pair '''

		if self.isSafeTableName(table) and self.isSafeColumnName(columnName) and self.isSafeMaxResults(maxResults) and self.isSafeSortOrder(sortOrder):
			query = "SELECT * from " + table + " ORDER BY " + columnName + " " + sortOrder + " LIMIT " + str(maxResults)
			
			self.c.execute(query)
			entries = self.c.fetchall()
			return entries
			

	def selectSingle(self, table, whereColumn, whereValue):
		''' Returns a single value for some table/column/value '''

		if self.isSafeTableName(table) and self.isSafeColumnName(whereColumn):
			query = "SELECT * from " + table + " WHERE " + whereColumn + " = ? LIMIT 1"

			self.c.execute(query, (whereValue,))
			entry = self.c.fetchone()
			return entry


	def selectAll(self, table):
		''' Returns all columns from a table '''

		if self.isSafeTableName(table):
			query = "SELECT * from " + table

			self.c.execute(query)
			entries = self.c.fetchall()
			return entries