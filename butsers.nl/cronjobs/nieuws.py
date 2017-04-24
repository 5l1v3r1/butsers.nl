import feedparser
import sqlite3
import time

dbFile = "../database/butsers.nl.db"


conn = sqlite3.connect(dbFile)
c = conn.cursor()

c.execute('SELECT id, sourceURL from nieuws_sources')
sources = c.fetchall()

for source in sources:
	sourceId, sourceURL = source

	RssFeed = feedparser.parse(sourceURL)

	for entry in RssFeed.entries:

		c.execute('SELECT id from nieuws_entries WHERE linkURL = ?', (entry.link, ))

		if c.fetchone() == None:
			
			# difference RSS 1.0 and 2.0
			if 'date_parsed' in entry:
				publishedStamp = time.mktime(entry.date_parsed)
			if 'published_parsed' in entry:
				publishedStamp = time.mktime(entry.published_parsed)

			c.execute('INSERT INTO nieuws_entries (sourceId, linkURL, linkDesc, linkPublished) VALUES (?, ?, ?, ?)', (sourceId, entry.link, entry.title, publishedStamp))
			conn.commit()


conn.commit()
conn.close()